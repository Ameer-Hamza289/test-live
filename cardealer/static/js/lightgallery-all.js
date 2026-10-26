/*! lightgallery - v1.6.12 - 2019-02-19
* http://sachinchoolur.github.io/lightGallery/
* Copyright (c) 2019 Sachin N; Licensed GPLv3 */
/*! lightgallery - v1.6.12 - 2019-02-19
* http://sachinchoolur.github.io/lightGallery/
* Copyright (c) 2019 Sachin N; Licensed GPLv3 */
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module unless amdModuleId is set
        define(['jquery'], function (a0) {
            return (factory(a0));
        });
    } else if (typeof module === 'object' && module.exports) {
        // Node. Does not work with strict CommonJS, but
        // only CommonJS-like environments that support module.exports,
        // like Node.
        module.exports = factory(require('jquery'));
    } else {
        factory(root["jQuery"]);
    }
}(this, function ($) {

    (function() {
        'use strict';

        var defaults = {

            mode: 'lg-slide',

            // Ex : 'ease'
            cssEasing: 'ease',

            //'for jquery animation'
            easing: 'linear',
            speed: 600,
            height: '100%',
            width: '100%',
            addClass: '',
            startClass: 'lg-start-zoom',
            backdropDuration: 150,
            hideBarsDelay: 6000,

            useLeft: false,

            closable: true,
            loop: true,
            escKey: true,
            keyPress: true,
            controls: true,
            slideEndAnimatoin: true,
            hideControlOnEnd: false,
            mousewheel: true,

            getCaptionFromTitleOrAlt: true,

            // .lg-item || '.lg-sub-html'
            appendSubHtmlTo: '.lg-sub-html',

            subHtmlSelectorRelative: false,

            /**
             * @desc number of preload slides
             * will exicute only after the current slide is fully loaded.
             *
             * @ex you clicked on 4th image and if preload = 1 then 3rd slide and 5th
             * slide will be loaded in the background after the 4th slide is fully loaded..
             * if preload is 2 then 2nd 3rd 5th 6th slides will be preloaded.. ... ...
             *
             */
            preload: 1,
            showAfterLoad: true,
            selector: '',
            selectWithin: '',
            nextHtml: '',
            prevHtml: '',

            // 0, 1
            index: false,

            iframeMaxWidth: '100%',

            download: true,
            counter: true,
            appendCounterTo: '.lg-toolbar',

            swipeThreshold: 50,
            enableSwipe: true,
            enableDrag: true,

            dynamic: false,
            dynamicEl: [],
            galleryId: 1
        };

        function Plugin(element, options) {

            // Current lightGallery element
            this.el = element;

            // Current jquery element
            this.$el = $(element);

            // lightGallery settings
            this.s = $.extend({}, defaults, options);

            // When using dynamic mode, ensure dynamicEl is an array
            if (this.s.dynamic && this.s.dynamicEl !== 'undefined' && this.s.dynamicEl.constructor === Array && !this.s.dynamicEl.length) {
                throw ('When using dynamic mode, you must also define dynamicEl as an Array.');
            }

            // lightGallery modules
            this.modules = {};

            // false when lightgallery complete first slide;
            this.lGalleryOn = false;

            this.lgBusy = false;

            // Timeout function for hiding controls;
            this.hideBartimeout = false;

            // To determine browser supports for touch events;
            this.isTouch = ('ontouchstart' in document.documentElement);

            // Disable hideControlOnEnd if sildeEndAnimation is true
            if (this.s.slideEndAnimatoin) {
                this.s.hideControlOnEnd = false;
            }

            // Gallery items
            if (this.s.dynamic) {
                this.$items = this.s.dynamicEl;
            } else {
                if (this.s.selector === 'this') {
                    this.$items = this.$el;
                } else if (this.s.selector !== '') {
                    if (this.s.selectWithin) {
