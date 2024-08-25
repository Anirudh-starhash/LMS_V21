<template>
    <div :class="[isDarkMode?'dark':'main-class']">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  
         <!-- header-->
          <librarian_header :showMonitor="false" :showLib="false" :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" />
  
  
        <div class="main-content">
           <h2 :class="[isDarkMode?'h2dark':'h2light']">Do you really want to Delete the book of ID {{this.book_id}}</h2>
           <div class="buttons">
            <button @click="deletebook" class="btn btn-success a">Yes</button>
            <button @click="back" class="btn btn-danger a">No</button>
           </div>
        </div>
  
        <!-- Footer -->
        <footer_page/>
  
        
       
    </div>
    
  
  </template>
  
  <script>
  import axios from 'axios'
  import { useRouter } from 'vue-router';
  import librarian_header from '../library_components/librarian_header.vue';
  import footer_page from '../other_components/footer_page.vue'
  export default {
     name: "delete_book",
     data(){
      return{
        request_status:'Currently No Requests Receive',
        stats_status:'Stats Page is up to date',
        monitor_status:'No Users to Monitor Currently',
        isDarkMode:false,
        book_id:"",
        section_id:""
      }
     },
     setup(){
        const router=useRouter();
        return {router};
     },
     components:{
      librarian_header,
      footer_page
     }, 
     methods: {
        toggleDarkMode(isDark) {
          this.isDarkMode = isDark;
        },
        back(){
            this.$router.push({name:"view_section",params:{id:this.section_id}});
        },
        async deletebook(){
            try{
                const r=await axios.post("http://127.0.0.1:5000/api/deleteBook",
                    JSON.stringify({
                      "book_id":this.book_id
                    }),
                    {
                      headers:{
                        'Content-Type':'application/json'
                       }
                    }
                );

                if(r.status===200){
                   this.$router.push({name:"view_section",params:{id:this.section_id}});
                }
            }
            catch(error){
                console.log(error);
            }
        }

  },
  async mounted(){
    const access_token=localStorage.getItem("access_token")
    if(!access_token){
      alert('You need to login first to come here!')
      this.$router.push("/librarian_page");
    }
    else{
        this.book_id=localStorage.getItem("book_id");
        this.section_id=localStorage.getItem("section_id");
        alert(this.book_id)
      try{
        const response=await axios.post("http://127.0.0.1:5000/api/lib_check_permission",null,
                    {
                        headers:{
                            Authorization:`Bearer ${access_token}`
                        }
                    }
         );
         if(response.status!==200){
            localStorage.removeItem("access_token");
            localStorage.removeItem("info");
            localStorage.removeItem("section_id")
            localStorage.removeItem("book_id")
            this.$router.push("/unauthorized");
         }

      }
      catch(error){
        console.log(error)
      }
    }
  }
  
  
  };
  </script> 
  
  
  <style scoped>
  
   .left,.right {
     float: left;
     width: 20%; /* The width is 20%, by default */
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
  .main-content{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap:40px;
    padding: 60px;
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