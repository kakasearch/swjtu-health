// ==UserScript==
// @name         西南交大健康填报
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  try to take over the world!
// @author       kaka
// @match        http://xgsys.swjtu.edu.cn/spcptest/web*
// @match        http://xgsys.swjtu.edu.cn/SPCPTest/Web*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    let id='20181231231'//学号
    let name='丁一'//名字
    let card='123123'//身份证后6位

    if(location.href=='http://xgsys.swjtu.edu.cn/spcptest/web/'||location.href=="http://xgsys.swjtu.edu.cn/SPCPTest/Web/"){
        if(id=='20181231231'){
            alert('j建议先前往代码处修改信息为你自己的')
            document.querySelector("#codeInput").value =document.querySelector("#code-box").innerText
        }else{
        document.querySelector("#StudentId").value =id;
        document.querySelector("#Name").value = name;
        document.querySelector("#IdCard").value = card;
        document.querySelector("#codeInput").value =document.querySelector("#code-box").innerText
        document.querySelector("#Submit").click()
        console.log('first page done')}
    }
    if(location.href=='http://xgsys.swjtu.edu.cn/SPCPTest/Web/Account/ChooseSys'){
        document.querySelector("#platfrom2 > a > img").click()
        console.log('已选择填报信息')
    }
    if(location.href=='http://xgsys.swjtu.edu.cn/SPCPTest/Web/Report/Index'){
        document.querySelector("#ckCLS").click()
        document.querySelector("#SaveBtnDiv > button").click()
        console.log('已提交')
    }
    // Your code here...
})();