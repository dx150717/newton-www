
function checkDirect(scheme, download_url) {
  if (!isMobile()) {
    window.location = download_url;
    return
  }
  
  var now = new Date().valueOf();
  setTimeout(function () {
    if (new Date().valueOf() - now > 100) return;
    window.location = download_url;
  }, 25);
  window.location = scheme;
}


function isMobile() {
  try {
    if(/Android|webOS|iPhone|iPad|iPod|pocket|psp|kindle|avantgo|blazer|midori|Tablet|Palm|maemo|plucker|phone|BlackBerry|symbian|IEMobile|mobile|ZuneWP7|Windows Phone|Opera Mini/i.test(navigator.userAgent)) {
      return true;
    }
    return false;
  } catch(e){ console.log("Error in isMobile"); return false; }
}

