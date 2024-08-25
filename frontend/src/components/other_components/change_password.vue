<template>
    <div v-bind:class="['abc',{dark:isDarkMode},{ 'dark-background': isDarkMode }]">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <div class="main">
        <h1>CHANGE PASSWORD PAGE
          <button @click="toggleDarkMode" class="btn btn-primary mt-3">
           <i v-if="isDarkMode" class="fas fa-sun"></i> <!-- Sun icon for light mode -->
           <i v-else class="fas fa-moon"></i> <!-- Moon icon for dark mode -->
         </button>
         <span class="c" v-if="isDarkMode"> &nbsp;Light Mode!</span>
         <span class="c" v-else> &nbsp; &nbsp; Dark Mode!</span></h1>
        <p>{{message}}</p>
        <div class="row">
          <form @submit.prevent="changePassword">
            <div class="mb-11 password-container">
              <label for="exampleInputPassword1" class="form-label"><p class="x">Old Password</p></label>
              <div class="input-group">
                <input type="password" class="form-control" id="exampleInputPassword1" v-model="old_password">
                <span class="input-group-text" id="togglePassword"><i class="fas fa-eye"></i></span>
              </div>
            </div>
            <div class="mb-11 password-container">
              <label for="exampleInputPassword2" class="form-label"><p class="x">New Password</p></label>
              <div class="input-group">
                <input type="password" class="form-control" id="exampleInputPassword2" v-model="new_password">
                <span class="input-group-text" id="togglePassword1"><i class="fas fa-eye"></i></span>
              </div>
            </div>
            <div class="mb-11 password-container">
              <label for="exampleInputPassword3" class="form-label"><p class="x">Confirm New Password</p></label>
              <div class="input-group">
                <input type="password" class="form-control" id="exampleInputPassword3" v-model="confirm_new">
                <span class="input-group-text" id="togglePassword2"><i class="fas fa-eye"></i></span>
              </div>
            </div>
            <button type="submit" class="btn btn-primary">Change Password</button>
          </form> 
        </div> 
        <div class="buttons">
          <div>
            <a href="/">
              <button :class="['btn', isDarkMode ? 'btn-dark' : 'btn-outline-primary', 'p-3', 'lh-1']">Home</button>
            </a>
          </div>
        </div>
      </div>
     
  
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { useRouter } from 'vue-router';
  export default {
   name:'change_password',
   setup(){
    const router=useRouter();
    return {router};
   },
   data(){
    return {
      message:'Welcome to Change Password Page',
      email:"",
      email_error:"",
      isDarkMode: false,
      old_password:"",
      new_password:"",
      confirm_new:""
    }
   },
   mounted() {
      const togglePassword = document.querySelector('#togglePassword');
      const password = document.querySelector('#exampleInputPassword1');
  
      togglePassword.addEventListener('click', function (e) {
        // Toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        // Toggle the eye slash icon
        this.querySelector('i').classList.toggle('fa-eye-slash');
      });
      const togglePassword1 = document.querySelector('#togglePassword1');
      const password1 = document.querySelector('#exampleInputPassword2');
  
      togglePassword1.addEventListener('click', function (e) {
        // Toggle the type attribute
        const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
        password1.setAttribute('type', type);
        // Toggle the eye slash icon
        this.querySelector('i').classList.toggle('fa-eye-slash');
      });
      const togglePassword2 = document.querySelector('#togglePassword2');
      const password2 = document.querySelector('#exampleInputPassword3');
  
      togglePassword2.addEventListener('click', function (e) {
        // Toggle the type attribute
        const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
        password2.setAttribute('type', type);
        // Toggle the eye slash icon
        this.querySelector('i').classList.toggle('fa-eye-slash');
      });
    },
    methods: {
      toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
      },
      async changePassword(){
        if(this.new_password==this.old_password){
          alert("Old Password and New Password can't be same");
          this.new_password=""
          this.confirm_new=""
        }
        if(this.new_password==this.confirm_new){
          const r=await axios.post("http://127.0.0.1:5000/api/change_password",
            JSON.stringify({
              'id':this.$route.params.id,
              'new_password':this.new_password,
              'old_password':this.old_password
            }),
            {
              headers:{
                'Content-Type':'application/json'
              }
            }
          );

          if(r.status==200){
            alert('Password Successfully changed!');
            this.$router.push(`/profile_page/${this.$route.params.id}`)
          }
          else if(r.status==201){
            alert('Your Password is Wrong enter correct one')
            this.old_password="";
            this.new_password="";
            this.confirm_new=""
          }
        }
        else{
          alert("Your new_password and confirm aren't same")
          this.new_password="";
          this.confirm_new=""

        }
      }
    }
  }
  </script>
  
  <style scoped>
  .abc {
    --bg-color:aliceblue;
    --text-color: black;
    --link-color: blue;
    --input-bg-color: white;
    --input-text-color: black;
    --button-bg-color: white;
    --button-text-color: black;
    --shadow-color:whitesmoke;
  }
  .dark {
    --bg-color: #2c2c2c;
    --text-color:  #6bb5ff;
    --link-color: black;
    --input-bg-color: whitesmoke;
    --input-text-color: black;
    --button-bg-color: #555;
    --button-text-color: #ffffff;
    --shadow-color:gainsboro;
  }
  
  
  
  .left, .right {
    float: left;
    width: 20%; /* The width is 20%, by default */
  }
  
  .main {
    float: left;
    width: 60%; /* The width is 60%, by default */
  }

  .dark .c{
    color:black;
  }
  
  /* Use a media query to add a breakpoint at 800px: */
  @media screen and (max-width: 800px) {
    .left, .main, .right {
      width: 100%; /* The width is 100%, when the viewport is 800px or smaller */
    }
  }
  
  .abc {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    min-width: 100%;
    background-image: url("../../assets/images/lib_login2.png");
    background-repeat: no-repeat;
    background-size: cover;
    background-color: var(--bg-color);
    color: var(--text-color);
  }
  
  
  .x:hover {
    transform: translate(2px);
  }
  
  .x {
    height: 40px;
  }
  
  .main {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 20px;
  }
  
  .row {
    box-sizing: border-box;
    box-shadow: 0 0 15px var(--shadow-color);
    width: 700px;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--bg-color);
    border-radius: 50px;
    cursor: pointer;
    font-size: 15px;
    padding: 40px;
  }
  
  .dark  {
    background-color: black;
    background-image: url("../../assets/images/section.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    width:100%;
  
  }
  .dark h1{
    color: white;
  }
  
  
  .buttons {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 40px;
  }
  
  form {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    gap: 40px;
    width: 500px;
  }
  
  p {
    color: var(--link-color);
  }
  
  h1, p, a {
    font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace;
    font-size: 40px;
    font-style: normal;
    font-variant: normal;
    font-weight: 700;
    line-height: 26.4px;
  }
  
  p, a {
    font-size: 24px;
  }
  
  .x,.c {
    font-size: 18px;
    color: var(--text-color);
  }
  
  .password-container .input-group {
    display: flex;
  }
  
  .password-container .input-group .input-group-text {
    cursor: pointer;
    background-color: var(--input-bg-color);
    color: var(--input-text-color);
  }
  </style>
  