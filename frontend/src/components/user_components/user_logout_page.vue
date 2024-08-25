<template>
    <div :class="[isDarkMode?'dark':'main-class']">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <user_header :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode"/>
        <div class="main-content">
          <h2 :class="[isDarkMode?'h2dark':'h2light']">Do you really want to Logout?</h2>
          <div class="buttons">
            <button @click="logout" class="btn btn-success a">Yes</button>
            <button @click="back" class="btn btn-danger a">No</button>
           </div>
        </div>
        <footer_page/>
       
    </div>
  
  </template>
  
  <script>
  import axios from 'axios'
  import { useRouter } from 'vue-router';
  import user_header from '../user_components/user_header.vue' 
  import footer_page from '../other_components/footer_page.vue'
  export default {
     name: "user_logout_page",
     setup(){
        const router=useRouter();
        return {router}
     },
     data(){
      return{
        request_status:'Currently No Requests Sent',
        stats_status:'Stats Page is up to date',
        issue_status:'No Books Issued Currently',
        return_status:'No Books to return Currently',
        isDarkMode:false,
        id:"",
      }
     },
     components:{
      user_header,
      footer_page
     },
     setup(){
      const router=useRouter();
      return {router};
     },
     methods: {
       toggleDarkMode(isDark) {
         this.isDarkMode = isDark;
       },
       back(){
            this.$router.push("/user_dashboard/`${id}`");
        },
        async logout(){
            const access_token=localStorage.getItem("access_token")
            try{
                const response=await axios.post("http://127.0.0.1:5000/api/user_logout",null,
                    {
                        headers:{
                            Authorization:`Bearer ${access_token}`
                        }
                    }
                );
                if(response.status===200){
                    localStorage.removeItem("access_token");
                    localStorage.removeItem("info");
                    localStorage.removeItem("book_id")
                    this.$router.push("/login_page");
                }
                else{
                    alert('Some Error!')
                }
            }catch(error){
                console.log(error)
            }
        }
      },
      async mounted() {
        const access_token=localStorage.getItem("access_token")
        if(!access_token){
          alert('You need to login first to come here!')
          this.$router.push("/login_page");
        }
        else{
          this.id=JSON.parse(localStorage.getItem("info")).id;
          try{
            const r=await axios.post("http://127.0.0.1:5000/api/user_check_permission",null,
              {
                headers:{
                  Authorization:`Bearer ${access_token}`
                }
              }
            );
            if(r.status===200){}
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
      }
  };
  </script> 
  
  
  <style scoped>
    .x{
        color: #fed7aa;
    }
    .x1{
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
    }
    .x:hover{
        background-color: transparent !important;
    }
   .left,.right {
     float: left;
     width: 20%; /* The width is 20%, by default */
  } 
  .add{
    margin-top: auto;
  }
  #add{ 
    width: 70px; 
    height: 70px; 
    padding: 10px 16px; 
    border-radius: 35px; 
    font-size: 30px; 
    text-align: center; 
  } 
  #add:hover{
    transform: translate(2px);
    background-color: blue;
    color: white;
  }
  
   .x{
    height: 40px;
    width: 100px;
   }
   .x:hover{
    transform: translate(2px);
    background-color: darkolivegreen;
    color:aliceblue;
   }
  
  .main {
    float: left;
    width: 60%; /* The width is 60%, by default */
  }
  
  /* Use a media query to add a breakpoint at 800px: */
   @media screen and (max-width: 800px) {
     .left,.main,.right {
         width: 100%; /* The width is 100%, when the viewport is 800px or smaller */
     } 
  }
  .buttons{
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 40px;
  }
  .a{
    width:100px;
  }
  h1 {
    color: salmon;
    text-align: center;
    font-family: foglghten;
    font-weight: bold;
    font-size: 40px;
  }
  p {
    color: darkblue;
    font-family: foglghten;
    font-size: 25px;
  }
  .center {
     display: flex;
     flex-direction: row;
     gap: 20px;
  }
  .image {
   align-items: center;
  }
  .container-fluid{
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: column;
  }
  .image {
   display: flex;
   flex-direction: column;
   align-items: center;
   width: 500px;
   margin-top: 150px;
  }
  .intro {
   display: flex;
   flex-direction: column;
   width: 70%;
  }
  .text {
   display: flex;
   flex-direction: column;
   align-items: center;
  }
  .row {
   font-size: 20px;
   color: blue;
   height: 100%;
   margin-top: 50px;
  }
  .main-class {
  display: flex;
  flex-direction: column;
  background-size: cover; 
  background-image: url('../../assets/images/lib_login2.png');
  background-repeat: no-repeat;
  min-height: 100vh;
  }
  
  .dark{
  display: flex;
  flex-direction: column;
  background-size: cover; 
  background-image: url('../../assets/images/section.jpg');
  background-repeat: no-repeat;
  min-height: 100vh;
  }
  span {
   color: red;
  }
  .main-content{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap:30px;
    padding: 20px;
  }
  .add{
    margin-top:auto;
    width:200px;
    height: 50px;
  }
  .add:hover{
    transform: translate(2px);
  }
  .h2light{
    font-size:22px;;
    color:darkblue;
    font-weight: bold;
    margin-bottom: auto;
  }
  .h2dark{
    font-size:22px;;
    color:black;
    font-weight: bold;
    margin-bottom: auto;
  }
  h2,p,a {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
  </style>