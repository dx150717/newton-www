/* index page videos js */
function initIndexVideos () {
    var videoPlayer1 = videojs('newton-video-1');
    var videoPlayer2 = videojs('newton-video-2');
    $("#video-tab-1").click(function () {
        videoPlayer2.pause();
        $("#newton-video-2").hide();
        $("#newton-video-1").show();
        $("#newton-video-1_html5_api").show();
        videojs("newton-video-1", {}, function() {
            window.videoPlayer1 = this;
            videoPlayer1.play();
        });
    });
    $("#video-tab-2").click(function () {
        videoPlayer1.pause();
        $("#newton-video-1").hide();
        if (!isiOS) {
            $("#newton-video-2").show();
            $("#newton-video-2_html5_api").show();
            videojs("newton-video-2", {}, function() {
                window.videoPlayer2 = this;
                videoPlayer2.play();
            });
        } else {
            var video = new tvp.VideoInfo();
            video.setVid("n0814ugqh49");
            var player =new tvp.Player();
            player.create({
                width:320,
                height:215,
                video:video,
                modId:"node-video-tencent2",
                autoplay:true,
            });
            player.onplay = function () {
                $("#video-tab-1").click(function () {
                    player.pause();
                });
            }
        }
    });
};

initIndexVideos();