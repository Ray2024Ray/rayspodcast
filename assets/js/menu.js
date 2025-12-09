/*
// 这是 assets/js/menu.js 的全部内容

(function(){
  var btn = document.getElementById('ccMenuBtn');
  var nav = document.getElementById('ccMainNav');
  
  // 确保按钮和菜单都存在
  if (!btn || !nav) {
    console.error('菜单按钮(ccMenuBtn)或菜单(ccMainNav)未找到。');
    return;
  }
  
  // 1. 汉堡按钮的点击事件
  btn.addEventListener('click', function(e){
    e.stopPropagation(); // 阻止事件冒泡
    
    // 一起切换菜单和按钮
    var open = nav.classList.toggle('is-open');
    btn.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  
  // 2. 点击菜单外部区域时，自动关闭菜单
  document.addEventListener('click', function(e){
    if (!nav.classList.contains('is-open')) {
      return; // 菜单是关闭的，什么也不做
    }
    
    var isClickInsideMenu = nav.contains(e.target);
    
    if (!isClickInsideMenu) {
      // 是的，点击了菜单外部
      nav.classList.remove('is-open');
      btn.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
    }
  });
})();
*/
// 文件结束
