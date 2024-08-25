


<template>
  <div v-bind:class="['abc',{dark:isDarkMode},{ 'dark-background': isDarkMode }]">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <librarian_header :showSections="false"  :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode"/>
    <div class="main">
      <h1>Add Section Page</h1>
      <p>{{message}}</p>
      <div class="row">
        <form @submit.prevent="addSection">
          <div class="mb-7">
            <label for="exampleInputEmail1" class="form-label"><p class="ch">Title</p></label>
            <input type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="title">
          </div>
          <div class="mb-7">
            <label for="exampleInputdate1" class="form-label"><p class="ch">Date</p></label>
            <input type="date" class="form-control" id="exampleInputdate1" v-model="date">
          </div>
          <div class="mb-7">
            <label for="exampleInputarea1" class="form-label"><p class="ch">Description</p></label>
            <input type="area" class="form-control" id="exampleInputarea1" v-model="description">
          </div>
          <div class="mb-7">
            <label for="exampleInputsecimg1" class="form-label"><p class="ch">Section Image URL</p></label>
            <input type="file" class="form-control" id="exampleInputsecimg1" @change="onFileChanges">
          </div>
          <button type="submit" class="btn btn-primary">Add</button>
        </form> 
      </div>
     <div class="buttons">
        <div>
          <a href="/section_page">
            <button :class="['btn', isDarkMode ? 'btn-dark' : 'btn-outline-primary', 'p-3', 'lh-1']">Section Page</button>
          </a>
        </div>
        <div>
          <a href="/librarian_dashboard">
            <button :class="['btn', isDarkMode ? 'btn-dark' : 'btn-outline-primary', 'p-3', 'lh-1']">Cancel</button>
          </a>
        </div>
      </div>
    </div>
    <footer_page/>

    
   

  </div>
</template>

<script>
  import librarian_header from '../library_components/librarian_header.vue'
  import footer_page from '../other_components/footer_page.vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router';
export default {

 name:'add_section',
 data(){
  return {
      message:"Welcome to Add Section Page",
      isDarkMode:false,
      title:"",
      description:"",
      date:"",
      img_url:""
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
  onFileChanges(event){
    const file = event.target.files[0];
      if (file) {
        this.img_url = file.name;
      } else {
        this.img_url = '';
      }
  },
  async addSection(){
    try{
      const response=await axios.post("http://127.0.0.1:5000/api/addSection",
        JSON.stringify({
          "title":this.title,
          "img_url":this.img_url,
          "date":this.date,
          "description":this.description
        }),{
          headers:{
              'Content-Type':'application/json'
            }
        }
      );

      if(response.status===200){
        this.$router.push("/section_page")
      }
      else{
        alert('Can\'t Add section as it might exist')
        this.title=""
        this.date=""
        this.description=""
        this.img_url=""
        this.$router.push("/add_section")
      }
    } catch(error){
     console.log(error)
    }
   }
  },
  async mounted(){
    const access_token=localStorage.getItem("access_token")
    if(!access_token){
      alert('You have to login First!')
      this.$router.push("/librarain_page")
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
      }
      catch(error){
        console.log(error)
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


   .abc {
    display: flex;
    flex-direction: column;
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
  
  .main{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
    padding: 20px;
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
  .dark .c{
    color:black;
  }
  .buttons{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 40px;
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
  form{
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    gap:15px;
    width:500px;
  }
  p {
    color: var(--link-color);
  }

  h1,h2,p,a {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
  p{
    font-size: 20px;
  }
  .ch{
    font-size: 18px;
    color: var(--text-color);
  }
</style>