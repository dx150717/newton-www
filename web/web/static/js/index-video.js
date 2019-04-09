/* index page videos js */
function initIndexVideos () {
//Video:video-list-(id)
//ApiID:video-list-(id)_html5_api
    var VideoNumber = $("#video_block").attr("video_sum");
    var VideoPlayerList = new Array(VideoNumber+1);

    VideoPlayerList.push(null);
    for(var video_id=0;video_id < VideoNumber;video_id++){
        var VideoObj = videojs('video-list-'+(video_id+1));
        VideoPlayerList[video_id+1] = VideoObj;
    }
    console.log(VideoPlayerList);

    $('.video-link').click(function(event){
        var videoID = $(this).attr("video_id");
        console.log("Current Video ID: " + videoID);

        for(var _video=0;_video<VideoNumber;_video++){
            console.log(_video+1);
            VideoPlayerList[_video+1].pause();
        }

        for(var _video_id=0;_video_id<VideoNumber;_video_id++){
            $('#video-list-'+(_video_id+1)).hide();
        }
        $('#video-list-'+videoID).show();
        $('#video-list-'+videoID+'_html5_api').show();
        videojs('video-list-'+videoID, {}, function() {
            var player = VideoPlayerList[videoID];
            window.player = this;
            player.play();
        });

    });
}
function NewtonVideoPlay(PlayID,VideoNumber,VideoIDList,ApiIDList,VideoList,VideoPlayer){
        console.log(VideoNumber);
        console.log(VideoPlayer);

//    var VideoList = ['','newton-video-1','newton-video-2'];
//    var VideoNumber = VideoList.length - 1; // Number Start From 1
//
//    var VideoIDList = ['','#newton-video-1','#newton-video-2'];
//    var ApiIDList=['','#newton-video-1_html5_api','#newton-video-2_html5_api'];

        for(var _video=1;_video<VideoNumber+1;_video++){
            VideoPlayer[_video].pause();
        }

//        $("#newton-video-2").hide();
        for(var _video_id=1;_video_id<VideoNumber+1;_video_id++){
            if(_video_id != PlayID)
                $(VideoIDList[_video_id]).hide();
        }
        $(VideoIDList[PlayID]).show();
        $(ApiIDList[PlayID]).show();
        videojs(VideoList[PlayID], {}, function() {
            var player = VideoPlayer[PlayID];
            window.player = this;
            player.play();
        });
}

initIndexVideos();
