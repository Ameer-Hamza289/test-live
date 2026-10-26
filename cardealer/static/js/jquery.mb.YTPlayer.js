/*___________________________________________________________________________________________________________________________________________________
 _ jquery.mb.components                                                                                                                             _
 _                                                                                                                                                  _
 _ file: jquery.mb.YTPlayer.src.js                                                                                                                  _
 _ last modified: 05/01/16 17.43                                                                                                                    _
 _                                                                                                                                                  _
 _ Open Lab s.r.l., Florence - Italy                                                                                                                _
 _                                                                                                                                                  _
 _ email: matteo@open-lab.com                                                                                                                       _
 _ site: http://pupunzi.com                                                                                                                         _
 _       http://open-lab.com                                                                                                                        _
 _ blog: http://pupunzi.open-lab.com                                                                                                                _
 _ Q&A:  http://jquery.pupunzi.com                                                                                                                  _
 _                                                                                                                                                  _
 _ Licences: MIT, GPL                                                                                                                               _
 _    http://www.opensource.org/licenses/mit-license.php                                                                                            _
 _    http://www.gnu.org/licenses/gpl.html                                                                                                          _
 _                                                                                                                                                  _
 _ Copyright (c) 2001-2016. Matteo Bicocchi (Pupunzi);                                                                                              _
 ___________________________________________________________________________________________________________________________________________________*/
var ytp = ytp || {};

function onYouTubeIframeAPIReady() {
    if( ytp.YTAPIReady ) return;
    ytp.YTAPIReady = true;
    jQuery( document ).trigger( "YTAPIReady" );
}

var getYTPVideoID = function( url ) {
    var videoID, playlistID;
    if( url.indexOf( "youtu.be" ) > 0 ) {
        videoID = url.substr( url.lastIndexOf( "/" ) + 1, url.length );
        playlistID = videoID.indexOf( "?list=" ) > 0 ? videoID.substr( videoID.lastIndexOf( "=" ), videoID.length ) : null;
        videoID = playlistID ? videoID.substr( 0, videoID.lastIndexOf( "?" ) ) : videoID;
    } else if( url.indexOf( "http" ) > -1 ) {
        //videoID = url.match( /([\/&]v\/([^&#]*))|([\\?&]v=([^&#]*))/ )[ 1 ];
        videoID = url.match( /[\\?&]v=([^&#]*)/ )[ 1 ];
        playlistID = url.indexOf( "list=" ) > 0 ? url.match( /[\\?&]list=([^&#]*)/ )[ 1 ] : null;
    } else {
        videoID = url.length > 15 ? null : url;
        playlistID = videoID ? null : url;
    }
    return {
        videoID: videoID,
        playlistID: playlistID
    };
};

( function( jQuery, ytp ) {

    jQuery.mbYTPlayer = {
        name: "jquery.mb.YTPlayer",
        version: "3.0.8",
        build: "5883",
        author: "Matteo Bicocchi",
        apiKey: "",
        defaults: {
            containment: "body",
            ratio: "auto", // "auto", "16/9", "4/3"
            videoURL: null,
            playlistURL: null,
            startAt: 0,
            stopAt: 0,
            autoPlay: true,
            vol: 50, // 1 to 100
            addRaster: false,
            mask: false,
            opacity: 1,
            quality: "default", //or “small”, “medium”, “large”, “hd720”, “hd1080”, “highres”
            mute: false,
            loop: true,
            showControls: true,
            showAnnotations: false,
            showYTLogo: true,
            stopMovieOnBlur: true,
            realfullscreen: true,
            mobileFallbackImage: null,
            gaTrack: true,
            optimizeDisplay: true,
            align: "center,center", // top,bottom,left,right
            onReady: function( player ) {}
        },
        /**
         *  @fontface icons
         *  */
        controls: {
            play: "P",
            pause: "p",
            mute: "M",
            unmute: "A",
            onlyYT: "O",
            showSite: "R",
            ytLogo: "Y"
        },
        controlBar: null,
        loading: null,
        locationProtocol: "https:",
        filters: {
            grayscale: {
                value: 0,
                unit: "%"
            },
            hue_rotate: {
                value: 0,
                unit: "deg"
            },
            invert: {
                value: 0,
                unit: "%"
            },
            opacity: {
                value: 0,
                unit: "%"
            },
            saturate: {
                value: 0,
                unit: "%"
            },
            sepia: {
                value: 0,
                unit: "%"
            },
            brightness: {
                value: 0,
                unit: "%"
            },
            contrast: {
                value: 0,
                unit: "%"
            },
            blur: {
                value: 0,
                unit: "px"
            }
        },
        /**
         *
         * @param options
         * @returns [players]
         */
        buildPlayer: function( options ) {
            return this.each( function() {
                var YTPlayer = this;
                var $YTPlayer = jQuery( YTPlayer );
                YTPlayer.loop = 0;
                YTPlayer.opt = {};
                YTPlayer.state = {};
                YTPlayer.filters = jQuery.mbYTPlayer.filters;
                YTPlayer.filtersEnabled = true;
                YTPlayer.id = YTPlayer.id || "YTP_" + new Date().getTime();
                $YTPlayer.addClass( "mb_YTPlayer" );
                var property = $YTPlayer.data( "property" ) && typeof $YTPlayer.data( "property" ) == "string" ? eval( '(' + $YTPlayer.data( "property" ) + ')' ) : $YTPlayer.data( "property" );
                if( typeof property != "undefined" && typeof property.vol != "undefined" ) property.vol = property.vol === 0 ? property.vol = 1 : property.vol;

                jQuery.extend( YTPlayer.opt, jQuery.mbYTPlayer.defaults, options, property );

                if( !YTPlayer.hasChanged ) {
                    YTPlayer.defaultOpt = {};
