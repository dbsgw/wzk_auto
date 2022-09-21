/*
 * @Description: 
 * @Author: 刘洋
 * @Date: 2022-09-21 10:17:36
 * @LastEditTime: 2022-09-21 10:19:25
 * @LastEditors: xxx
 */
/*

登录自己武软公共课的账号 => 点击开始学习页面 => f12打开控制台  输入下面代码  完事（这里稍微等几秒在去关闭页面）

问题：大数据课程刷不了（我没选大数据课程就 没研究）
*/

// 完整案例
function geturlparam(url) {
    var p = url.split("?")[1];
    var params = new URLSearchParams(p);
    console.log(params.get("type")); //1
    console.log(params.get("id")); //2
    return {
      cpid: params.get("mid"),
      courseid: params.get("id"),
      stepid: params.get("sid"),
      courseClassId: params.get("courseClassId"),
    };
  }
  
  var domAll = document.querySelectorAll(
    ".c-outline-modules-container .h4.c-font-normal> a:nth-child(1)"
  );
  domAll.forEach((ele) => {
    var href = ele.href;
    if (href.includes("CoursePlay.aspx")) {
      var {cpid,courseid,stepid,courseClassId} = geturlparam(href);
      // 组装 url
      var url = `http://wrggk.whvcse.edu.cn/Viewer/timetop.aspx?cpid=${cpid}&bjtime=408.917333&courseid=${courseid}&stepid=${stepid}&courseClassId=${courseClassId}&t=0.02508191914463187`;
  
      // 发送请求
      $.post(url, function (data) {
        console.log(data);
      });
    }
  });