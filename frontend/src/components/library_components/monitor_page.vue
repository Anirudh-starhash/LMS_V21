<template>
  <div :class="[isDarkMode?'dark':'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

       <!-- header-->
        <librarian_header :showMonitor="false" :showLib="false" :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" />


      <div class="main-content">
        <ul class="list-unstyled">
          <li v-for="user in user_list" :key="user.user_id">
            <div class="card mb-5 color" style="max-width: 500px;">
              <div class="row g-0">
                <div v-if="profileexists(user.profile_pic)" class="col-md-12 image">
                  <img
                    :src="'../../../src/assets/images/'+user.profile_pic"
                    alt="Profile Pic"
                  />
                </div>
                <div v-else class="col-md-12 image">
                  <img
                    :src="'../../../src/assets/images/empty_user.jpg'"
                    alt="Profile Pic"
                  />
                </div>
                <div class="col-md-12">
                  <div class="card-body">
                    <div class="row1">
                      <div class="label">Name:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.name }}</div>
                    </div>
                    <div class="row1">
                      <div class="label">Email:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.email }}</div>
                    </div>
                    <div class="row1">
                      <div class="label">User ID:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.user_id }}</div>
                    </div>
                    <div class="row1">
                      <div class="label">Type:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.type }}</div>
                    </div>
                    <div class="row1">
                      <div class="label">Books Issued:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.issued_count }}</div>
                    </div>
                    <div class="row1">
                      <div class="label">Books Returned:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.return_count }}</div>
                    </div>
                    <div class="row1">
                      <div class="label">Books Requested:</div>
                      <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ user.req_count }}</div>
                    </div>
                    
                   
                  </div>
                  <div class="contact">
                    <a @click="emailthem(user.email)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-at-fill x blue" viewBox="0 0 16 16">
                        <path d="M2 2A2 2 0 0 0 .05 3.555L8 8.414l7.95-4.859A2 2 0 0 0 14 2zm-2 9.8V4.698l5.803 3.546zm6.761-2.97-6.57 4.026A2 2 0 0 0 2 14h6.256A4.5 4.5 0 0 1 8 12.5a4.49 4.49 0 0 1 1.606-3.446l-.367-.225L8 9.586zM16 9.671V4.697l-5.803 3.546.338.208A4.5 4.5 0 0 1 12.5 8c1.414 0 2.675.652 3.5 1.671"/>
                        <path d="M15.834 12.244c0 1.168-.577 2.025-1.587 2.025-.503 0-1.002-.228-1.12-.648h-.043c-.118.416-.543.643-1.015.643-.77 0-1.259-.542-1.259-1.434v-.529c0-.844.481-1.4 1.26-1.4.585 0 .87.333.953.63h.03v-.568h.905v2.19c0 .272.18.42.411.42.315 0 .639-.415.639-1.39v-.118c0-1.277-.95-2.326-2.484-2.326h-.04c-1.582 0-2.64 1.067-2.64 2.724v.157c0 1.867 1.237 2.654 2.57 2.654h.045c.507 0 .935-.07 1.18-.18v.731c-.219.1-.643.175-1.237.175h-.044C10.438 16 9 14.82 9 12.646v-.214C9 10.36 10.421 9 12.485 9h.035c2.12 0 3.314 1.43 3.314 3.034zm-4.04.21v.227c0 .586.227.8.581.8.31 0 .564-.17.564-.743v-.367c0-.516-.275-.708-.572-.708-.346 0-.573.245-.573.791"/>
                      </svg>
                    </a>
                    <p class="x2">Any queries Email Them</p>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Footer -->
      <footer_page/>

      
     
  </div>
  

</template>

<script>
import librarian_header from './librarian_header.vue';
import footer_page from '../other_components/footer_page.vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
export default {
   name: "monitor_page",
   data(){
    return{
      request_status:'Currently No Requests Receive',
      stats_status:'Stats Page is up to date',
      monitor_status:'No Users to Monitor Currently',
      isDarkMode:false,
      user_list:[]
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
    profileexists(img){
            if(img){
                return true;
            }
            else{
                return false;
            }
    },
    emailthem(email){

    }
  },
  async mounted() {
      const access_token=localStorage.getItem("access_token")
      if(!access_token){
        alert('You need to login first to come here!')
        this.$router.push("/librarian_page");
      }
      else{
        try{
          const r=await axios.post("http://127.0.0.1:5000/api/lib_check_permission",null,
            {
              headers:{
                Authorization:`Bearer ${access_token}`
              }
            }
          );
          if(r.status===200){
             // write when you code this page
             const response=await axios.get(`http://127.0.0.1:5000/api/getAllUserDetails`);
             this.user_list=response.data.user_list
            //  alert(JSON.stringify(response.data.user_list))
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


};
</script> 


<style scoped>

 .left,.right {
   float: left;
   width: 20%; /* The width is 20%, by default */
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
.x{
  height: 30px;
  width: 100px;
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
  margin-bottom: auto;
}
.h2dark{
  font-size:22px;;
  color:black;
  margin-bottom: auto;
}
.image img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}
.card-body {
  display: flex;
  flex-direction: column;
  gap: 16px; /* Reduced gap between rows */
}

.row1 {
  font-size: 20px;
  color: blue;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-content: center;
  gap: 20px;
}
.list-unstyled{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}
.color{
  background-color: aliceblue;
}
.card{
  padding:20px;
}
h2,p,a,.value,.label {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
.image {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
.value,.label{
  font-size:20px;
}
.x2{
  font-size: 18px;
  color: red;
}
.x:hover{
  transform: translate(10px);
}
.blue{
  color: blue;
 }
 .contact{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap:20px;
 }
</style>