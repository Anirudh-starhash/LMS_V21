<template>
    <div v-bind:class="['abc',{dark:isDarkMode},{ 'dark-background': isDarkMode }]">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <div class="main">
        <h1>REGISTER PAGE
          <button @click="toggleDarkMode" class="btn btn-primary mt-3">
           <i v-if="isDarkMode" class="fas fa-sun"></i> <!-- Sun icon for light mode -->
           <i v-else class="fas fa-moon"></i> <!-- Moon icon for dark mode -->
         </button>
         <span class="c" v-if="isDarkMode"> &nbsp; &nbsp; Light Mode!</span>
        <span class="c" v-else> &nbsp; &nbsp; Dark Mode!</span>
        </h1>
        <p>{{message}}</p>
        <div class="row">
          <form method="post" @submit.prevent="user_register">
            <div class="mb-7">
              <label for="exampleInputfirst name1" class="form-label"><p class="x">First Name</p></label>
              <input type="text" class="form-control" id="exampleInputfirstname1" aria-describedby="emailHelp" required v-model="firstname">
            </div>
            <div class="mb-7">
              <label for="exampleInputlastname1" class="form-label"><p class="x">Last Name</p></label>
              <input type="text" class="form-control" id="exampleInputlastname1" aria-describedby="emailHelp" required v-model="lastname">
            </div>
            <div class="mb-7">
              <label for="exampleInputEmail1" class="form-label"><p class="x">Email address</p></label>
              <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" required v-model="email">
            </div>
            <div class="mb-7">
              <label for="exampleInputEmail1" class="form-label"><p class="x">Profile Pic</p></label>
              <input type="file" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" @change="onFileChanges1">
            </div>
            <div v-if="email_error">Email not properly Formatted</div>
            <div class="mb-7 password-container">
              <label for="exampleInputPassword1" class="form-label"><p class="x">Password</p></label>
              <div class="input-group">
                <input type="password" class="form-control" id="exampleInputPassword1" v-model="password">
                <span class="input-group-text" id="togglePassword"><i class="fas fa-eye"></i></span>
              </div>
            </div>
            <div class="mb-7 password-container">
              <label for="exampleInputPassword2" class="form-label"><p class="x">Confirm Password</p></label>
              <div class="input-group">
                <input type="password" class="form-control" id="exampleInputPassword2" v-model=confirm_password>
                <span class="input-group-text" id="togglePassword1"><i class="fas fa-eye"></i></span>
              </div>
            </div>
            <div class="mb-7">
              <label for="ChooseYourDegree" class="form-label"> <p class="x">Choose Your Degree</p></label> <br>
              <select name="" id="ChooseYourDegree"  v-model="type" required>
                <option value="" disabled>select a degree</option>
                <option value="ug">Under Graduate</option>
                <option value="pg">Post Graduate</option>
                <option value="phd">PHD</option>
                <option value="rs">Research Scholar</option>
                <option value="fac">Faculty</option>
              </select>
            </div>
            <button @click="signupUser" type="submit" class="btn btn-primary">Register</button>
          </form> 
        </div>
        <div class="buttons">
          <div>
            <a href="/login_page">
              <button :class="['btn', isDarkMode ? 'btn-outline-dark' : 'btn-outline-primary', 'p-3', 'lh-1']">Login</button>
            </a>
          </div>
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
   name:'register_page',
   data(){
    return {
      message:'Welcome to Register Page',
      email:"",
      email_error:"",
      isDarkMode: false,
      password:"",
      lastname:"",
      firstname:"",
      type:"",
      confirm_password:"",
      profile_pic:""
    }
   },
   setup(){
    const router=useRouter()
    return {router}
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
    },
    methods: {
      toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
      },
      onFileChanges1(event){
          const file = event.target.files[0];
            if (file) {
              this.profile_pic = file.name;
            } else {
              this.profile_pic = '';
            }
        },
      async user_register(){
        try{
          if(this.confirm_password!==this.password){
            alert('Password and Confirm Password didn\'t match')
            this.confirm_password="";
            this.$router.push("/register_page")
          }
          else{
          const response=await axios.post("http://127.0.0.1:5000/api/user_register",
            JSON.stringify({
              firstname:this.firstname,
              lastname:this.lastname,
              email:this.email,
              password:this.password,
              type:this.type,
              profile_pic:this.profile_pic
            }),{
              headers:{
                'Content-Type':'application/json'
              }
            }
          );

          if(response.status===200){
            this.$router.push("/login_page")
          }
          else{
            alert('Redirecting Login Page already Registered!')
            this.$router.push("/login_page")
          }}
        }catch(error){
          console.log(error);
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
  
  /* Use a media query to add a breakpoint at 800px: */
  @media screen and (max-width: 800px) {
    .left, .main, .right {
      width: 100%; /* The width is 100%, when the viewport is 800px or smaller */
    }
  }
  
  .dark .c{
    color:black;
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
    margin-right:100px;
    gap:40px;
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
  