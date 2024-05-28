使用Python selenium登录企业微信管理界面
自动设置动态IP到应用可信IP

使用方法:
  浏览器常规登录企业微信后,进入到要设置可信IP的应用界面,复制浏览器网址
  大概是这样一个网址https://work.weixin.qq.com/wework_admin/frame#/apps/modApiApp/5629501223702671
  
  使用浏览器cookie插件(([Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm))导出HeaderString格式的cookie
  
  把应用网址和cookie填入weworkIP.py文件里的对应设置
  
  运行py文件,脚本会根据设定的时间间隔来检测当前ip地址,如果有变化则更改到可信ip里面
