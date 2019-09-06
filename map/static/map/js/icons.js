/**
 * demo.js
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2016, Codrops
 * http://www.codrops.com
 */
var ajaxRequestIsProcessing = false;

function isIOSSafari() {
    var userAgent;
    userAgent = window.navigator.userAgent;
    return userAgent.match(/iPad/i) || userAgent.match(/iPhone/i);
}

// taken from mo.js demos
function isTouch() {
    var isIETouch;
    isIETouch = navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
    return [].indexOf.call(window, 'ontouchstart') >= 0 || isIETouch;
}

// taken from mo.js demos
var isIOS = isIOSSafari(),
    clickHandler = isIOS || isTouch() ? 'touchstart' : 'click';

function extend(a, b) {
    for (var key in b) {
        if (b.hasOwnProperty(key)) {
            a[key] = b[key];
        }
    }
    return a;
}

function Animocon(el, options) {
    this.el = el;
    this.options = extend({}, this.options);
    extend(this.options, options);
    this.checked = false;

    this.timeline = new mojs.Timeline();

    for (var i = 0, len = this.options.tweens.length; i < len; ++i) {
        this.timeline.add(this.options.tweens[i]);
    }

    var self = this;
    this.el.addEventListener(clickHandler, function () {
        if (self.checked) {
            self.options.onUnCheck();
        } else {
            self.options.onCheck();
            self.timeline.replay();
        }
        self.checked = !self.checked;
    });
}


Animocon.prototype.options = {
    tweens: [
        new mojs.Burst({})
    ],
    onCheck: function () {
        return false
    },
    onUnCheck: function () {
        return false
    }
};

function estimateMarker(markerId, vote) {
    ajaxRequestIsProcessing = true;
    var voteId = null;
    if (vote.toUpperCase() === 'LIKE') {
        voteId = 1;
    } else if (vote.toUpperCase() === 'DISLIKE') {
        voteId = -1;
    } else {
        voteId = 0;
    }
    var data = {
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'marker_id': markerId,
        'vote': voteId
    };
    $.ajax({
        method: 'POST',
        url: '/map/estimate_marker/',
        data: data,
        dataType: 'json',
        success: function (response) {
            if (response.user_is_logged === 'no') {
                window.location.replace('/auth/login/')
            } else {
                $('.like-counter').html(response.like_count);
                $('.dislike-counter').html(response.dislike_count);
            }
        },
        error: function (error) {
            console.log(error)
        }
    });
    ajaxRequestIsProcessing = false;
}

// icons:

function statusBtnsInit(markerId, checkedBtn = '') {
    var items = [].slice.call(document.querySelectorAll('div.like-dislike-block > .grid__item'));

    /* Dislike Icon  */
    var el1 = items[1].querySelector('button.icobutton'), el1span = el1.querySelector('span');
    var dislike = new Animocon(el1, {
        tweens: [
            // burst animation
            new mojs.Burst({
                parent: el1,
                radius: {30: 80},
                count: 6,
                children: {
                    fill: '#C0C1C3',
                    opacity: 0.6,
                    radius: 10,
                    duration: 1700,
                    easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
                }
            }),
            // ring animation
            new mojs.Shape({
                parent: el1,
                type: 'circle',
                radius: {0: 40},
                fill: 'transparent',
                stroke: '#C0C1C3',
                strokeWidth: {20: 0},
                opacity: 0.6,
                duration: 700,
                easing: mojs.easing.sin.out
            }),
            // icon scale animation
            new mojs.Tween({
                duration: 1200,
                onUpdate: function (progress) {
                    if (progress > 0.3) {
                        var elasticOutProgress = mojs.easing.elastic.out(1.43 * progress - 0.43);
                        el1span.style.WebkitTransform = el1span.style.transform = 'scale3d(' + -elasticOutProgress + ',' + elasticOutProgress + ',1)';
                    } else {
                        el1span.style.WebkitTransform = el1span.style.transform = 'scale3d(-1,1,1)';
                    }
                }
            })
        ],
        onCheck: function () {
            if (ajaxRequestIsProcessing === false) {
                $('.dislike').removeClass('text-dark').addClass('text-danger');
                $('.like').removeClass('text-primary');
                estimateMarker(markerId, 'dislike')
            }
        },
        onUnCheck: function () {
            if (ajaxRequestIsProcessing === false) {
                $('.dislike').removeClass('text-danger').addClass('text-dark');
                estimateMarker(markerId, '')
            }
        }
    });
    /* Dislike Icon */

    /* Like Icon */
    var el2 = items[0].querySelector('button.icobutton'), el2span = el2.querySelector('span');
    var like = new Animocon(el2, {
        tweens: [
            // burst animation
            new mojs.Burst({
                parent: el2,
                count: 6,
                radius: {40: 80},
                children: {
                    fill: ['#988ADE', '#DE8AA0', '#8AAEDE', '#8ADEAD', '#DEC58A', '#8AD1DE'],
                    opacity: 0.6,
                    scale: 1,
                    radius: {7: 0},
                    duration: 1500,
                    delay: 300,
                    easing: mojs.easing.bezier(0.1, 1, 0.3, 1)
                }
            }),
            // ring animation
            new mojs.Shape({
                parent: el2,
                type: 'circle',
                scale: {0: 1},
                radius: 40,
                fill: 'transparent',
                stroke: '#988ADE',
                strokeWidth: {35: 0},
                opacity: 0.6,
                duration: 750,
                easing: mojs.easing.bezier(0, 1, 0.5, 1)
            }),
            // icon scale animation
            new mojs.Tween({
                duration: 1100,
                onUpdate: function (progress) {
                    if (progress > 0.3) {
                        var elasticOutProgress = mojs.easing.elastic.out(1.43 * progress - 0.43);
                        el2span.style.WebkitTransform = el2span.style.transform = 'scale3d(' + elasticOutProgress + ',' + elasticOutProgress + ',1)';
                    } else {
                        el2span.style.WebkitTransform = el2span.style.transform = 'scale3d(0,0,1)';
                    }
                }
            })
        ],
        onCheck: function () {
            if (ajaxRequestIsProcessing === false) {
                $('.like').removeClass('text-dark').addClass('text-primary');
                $('.dislike').removeClass('text-danger');
                estimateMarker(markerId, 'like')
            }
        },
        onUnCheck: function () {
            if (ajaxRequestIsProcessing === false) {
                $('.like').removeClass('text-primary').addClass('text-dark');
                estimateMarker(markerId, '')
            }
        }
    });
    /* Like Icon */
    if (checkedBtn.toUpperCase() === 'LIKE') {
        like.checked = true;
    } else if (checkedBtn.toUpperCase() === 'DISLIKE') {
        dislike.checked = true;
    }
}
