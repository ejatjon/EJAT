//验证表单是否为空，若为空则将焦点聚焦在input表单上，否则表单通过，登录成功
function check_code() {
    var username_error=true
      console.log(1);
      var login_error=document.getElementById("logenChackMsg")
      login_error.innerText=""
      //获取账号
      var username =
        document.getElementById("logenUserName").value;
      //校验其格式(\w字母或数字或下划线)
      var a =
        document.getElementById("logenUserNameChackMsg");
      var reg = /^\w{1,32}$/;
      if(!username || username===""){
          a.innerText="pleas input user name!"
          return username_error
      }
      else {
           if(reg.test(username)) {
            //通过，增加ok样式
            a.innerText=''
               username_error=false
               return username_error
          } else {
            //不通过输出联机玩
            a.innerText = "pleas input number or letter! ";
            return username_error
          }
      }

    }
    function check_pwd(){
    var password_error=true
      console.log(2);
      var login_error=document.getElementById("logenChackMsg")
      login_error.innerText=""
      var password =document.getElementById("logenPassword").value;
      var a =
        document.getElementById("logenPasswordChackMsg");
      var reg2 = /^\w{6,18}$/;
      if(!password || password===''){
          a.innerText='Forgot password?'
          return password_error
      }else{
          if(reg2.test(password)) {
                a.innerText=""
                password_error=false
                return password_error

      } else {
        a.innerText="pleas input number or letter! ";
        return password_error
      }
      }






    }
function on_submit(){
    var username_error=check_code()
    var password_error=check_pwd()
    if(username_error===true||password_error===true){
        window.event.returnValue=false;
    }

}