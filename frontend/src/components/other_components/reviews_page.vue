<template>
    <div v-bind:class="['abc',{dark:isDarkMode},{ 'dark-background': isDarkMode }]">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <div class="main">
        <h1>User Reviews Page 
           <button @click="toggleDarkMode" class="btn btn-primary mt-3">
            <i v-if="isDarkMode" class="fas fa-sun"></i> <!-- Sun icon for light mode -->
            <i v-else class="fas fa-moon"></i> <!-- Moon icon for dark mode -->
          </button>
          <span class="c" v-if="isDarkMode"> &nbsp; &nbsp; Light Mode!</span>
          <span class="c" v-else> &nbsp; &nbsp; Dark Mode!</span>
        </h1>
        <p>{{message}}</p>
        <div class="row">
          <form @submit.prevent="submitreview">
            <div class="mb-7">
              <label for="exampleInputEmail1" class="form-label"><p class="x">Review</p></label>
              <input type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="review" required>
            </div>
            <div class="mb-7">
              <label for="ratings" class="form-label"><p class="x">Ratings out of 5</p></label>
              <div class="input-group">
                <input type="number" class="form-control" id="exampleInputPassword1" v-model="ratings">
              </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit Review</button>
          </form> 
        </div>
        <div class="buttons">
          <div>
            <a @click="cancel">
              <button :class="['btn', isDarkMode ? 'btn-dark' : 'btn-outline-primary', 'p-3', 'lh-1']">Cancel</button>
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
   name:'reviews_page',
   data(){
    return {
      message:'Welcome to Reviews Page',
      review:"",
      email_error:"",
      isDarkMode: false,
      ratings:"",
      id:"",
      book_id:""
     
    }
   },
   async mounted() {
      const access_token=localStorage.getItem("access_token")
      if(!access_token){
        alert('You need to login first to come here!')
        this.$router.push("/librarian_page");
      }
      else{
        this.id=JSON.parse(localStorage.getItem("info")).id,
        this.book_id=localStorage.getItem("book_id")
        try{
          const r=await axios.post("http://127.0.0.1:5000/api/user_check_permission",null,
            {
              headers:{
                Authorization:`Bearer ${access_token}`
              }
            }
          );
          if(r.status===200){
            var userInfo = JSON.parse(localStorage.getItem('info'));
            var userId = userInfo.id;
            var userdashlink = document.getElementById('backtouserdash');
            userdashlink.href = "/user_dashboard/" + userId;
          }
          else{
            localStorage.removeItem("access_token")
            localStorage.removeItem("info")
            localStorage.removeItem("book_id")
            localStorage.removeItem("section_id")
            this.$router.push("/unauthorized");
          }
        }
        catch(error){
          console.log(error);
        }
      }
      

    },
    setup(){
      const router=useRouter();
      return {router};
    },
    methods: {
      toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
      },
      async submitreview(){
        try{
          const r=await axios.post("http://127.0.0.1:5000/api/submitReview",
            JSON.stringify({
              "user_id":this.id,
              "book_id":this.book_id,
              "review":this.review,
              "ratings":this.ratings
            }),
            {
              headers:{
                'Content-Type':'application/json'
              }
            }
          );

          if(r.status===200){
            this.$router.push({name:'my_books_page',params:{id:this.id}});
          }
          else{
            alert('Some error!')
          }

        }
        catch(error){
          console.log(error)
        }
      }
    },
    cancel(){
      this.$router.push({name:'my_books_page',params:{id:this.id}});
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
  
  .x,.c {
    height: 40px;
  }
  .dark .c{
    color:black;
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
    font-size: 20px;
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
  