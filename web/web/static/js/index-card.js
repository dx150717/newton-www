  function hasClass(el, className) {
    if (el.classList)
      return el.classList.contains(className)
    else
      return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))
  }
  function addClass(el, className) {
    if (el.classList)
      el.classList.add(className)
    else if (!hasClass(el, className)) el.className += " " + className
  }
  function removeClass(el, className) {
    if (el.classList)
      el.classList.remove(className)
    else if (hasClass(el, className)) {
      var reg = new RegExp('(\\s|^)' + className + '(\\s|$)')
      el.className=el.className.replace(reg, ' ')
    }
  }
  //  Start
  showSplash()
  function showSplash() {
    removeClass(document.getElementById('splashmask'), 'hidewrapper');
    addClass(document.getElementById('splashmask'), 'splash_in');
    addClass(document.getElementById('cardctn'), 'animate_in');
  }
  //  Close
  function hideSplash() {
    addClass(document.getElementById('cardctn'), 'before_out');
    addClass(document.getElementById('cardctn'), 'animate_out');
    addClass(document.getElementById('splashmask'), 'splash_out');
    removeClass(document.getElementById('splashmask'), 'splash_in');
    setTimeout(function() {
      addClass(document.getElementById('splashmask'), 'hidewrapper');
      removeClass(document.getElementById('splashmask'), 'splash_in');
      removeClass(document.getElementById('cardctn'), 'animate_in');
      removeClass(document.getElementById('cardctn'), 'before_out');
      removeClass(document.getElementById('cardctn'), 'animate_out');
      removeClass(document.getElementById('splashmask'), 'splash_out');
    }, 1500);
  }


  var items = [
  "https://aris.la/temp/transparent.png",
  "https://images.unsplash.com/photo-1527409335569-f0e5c91fa707?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
  "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1952&q=80",
  "https://images.unsplash.com/photo-1529973625058-a665431328fb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
  "https://images.unsplash.com/photo-1537420327992-d6e192287183?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
  "https://images.unsplash.com/photo-1500212802521-de7d7426f496?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80",
  "https://images.unsplash.com/photo-1457365050282-c53d772ef8b2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80"
  ];

  function randomBg() {
    var item = "url(" + items[Math.floor(Math.random()*items.length)] + ")";
    //.write(item);
    document.getElementById('cardtitle').style.backgroundImage=item;
  }
  randomBg()