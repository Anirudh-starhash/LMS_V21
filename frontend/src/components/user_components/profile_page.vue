<template>
    <div :class="[isDarkMode ? 'dark' : 'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <user_header :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" :showProfile="false"/>
      <div class="main-content">
        <div v-if="profileexists" class="image">
          <img :src="'../../../src/assets/images/' + this.profile_details.profile_pic" alt="">
        </div>
        <div v-else class="image">
          <img :src="'../../../src/assets/images/empty_user.jpg'" alt="">
        </div>
        <div class="content">
          <div class="row1">
            <div class="label">Name:</div>
            <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ this.profile_details.name }}</div>
          </div>
          <div class="row1">
            <div class="label">Email:</div>
            <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ this.profile_details.email }}</div>
          </div>
          <div class="row1">
            <div class="label">User ID:</div>
            <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ this.profile_details.user_id }}</div>
          </div>
          <div class="row1">
            <div class="label">Type:</div>
            <div class="value" :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ this.profile_details.type }}</div>
          </div>
          <div class="row1">
            <a :href="'/change_password/'+this.profile_details.user_id">
              <button :class="['btn', isDarkMode ? 'btn-dark' : 'btn-outline-primary', 'p-3', 'lh-1']">Change Password</button>
            </a>
          </div>
        </div>
        <div class="buttons">
            <a @click="editProfile">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill x1 blue" viewBox="0 0 16 16">
                    <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
                </svg>
            </a>
            <p class="x2 blue">Edit Profile</p>
        </div>
      </div>
      <footer_page/>
    </div>
  </template>
  
  <script>
  import user_header from '../user_components/user_header.vue'
  import footer_page from '../other_components/footer_page.vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router';
  
  export default {
    name: "profile_page",
    data() {
      return {
        request_status: 'Currently No Requests Sent',
        stats_status: 'Stats Page is up to date',
        issue_status: 'No Books Issued Currently',
        return_status: 'No Books to return Currently',
        isDarkMode: false,
        id: "",
        profile_details: []
      }
    },
    components: {
      user_header,
      footer_page
    },
    methods: {
      toggleDarkMode(isDark) {
        this.isDarkMode = isDark;
      },
      editProfile(){
        this.$router.push({name:'edit_profile_page',params:{id:this.id}});
      }
    },
    computed:{
        profileexists(){
            if(this.profile_details.profile_pic){
                return true;
            }
            else{
                return false;
            }
        }
    },
    async mounted() {
      const access_token = localStorage.getItem("access_token")
      if (!access_token) {
        alert('You need to login first to come here!')
        this.$router.push("/librarian_page");
      } else {
        this.id = JSON.parse(localStorage.getItem("info")).id
        try {
          const r = await axios.post("http://127.0.0.1:5000/api/user_check_permission", null, {
            headers: {
              Authorization: `Bearer ${access_token}`
            }
          });
          if (r.status === 200) {
            const response = await axios.get(`http://127.0.0.1:5000/api/getProfile/${this.id}`);
            this.profile_details = response.data.profile_details
          } else {
            localStorage.removeItem("access_token")
            localStorage.removeItem("info")
            localStorage.removeItem("book_id")
            localStorage.removeItem("section_id")
            this.$router.push("/unauthorized");
          }
        } catch (error) {
          console.log(error);
        }
      }
    },
    setup() {
      const router = useRouter();
      return { router };
    },
  };
  </script>
  
  <style scoped>
  .x1,.x2{
    color: #fed7aa;
    text-align: center;
    height: 30px;
    width: 100px;
    font-size: 16px;
  }
  .x2{
    color:darkblue;
  }
  .left, .right {
    float: left;
    width: 20%;
  }
  .main {
    float: left;
    width: 60%;
  }
  @media screen and (max-width: 800px) {
    .left, .main, .right {
      width: 100%;
    }
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
  .container-fluid {
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
  .buttons{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap:10px;
  }
  .text {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .row1 {
    font-size: 20px;
    color: blue;
    height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-content: center;
    gap: 10px;
  }
  .main-class {
    display: flex;
    flex-direction: column;
    background-size: cover;
    background-image: url('../../assets/images/lib_login2.png');
    background-repeat: no-repeat;
    min-height: 100vh;
  }
  .dark {
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
  .main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: left;
    gap: 30px;
    padding: 20px;
    flex-direction: column;
    min-height: 100vh;
  }
  .image {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }
  .image img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
  }
  .x1{
    color: #fed7aa;
    text-align: center;
    height: 30px;
    width: 100px;
    font-size: 16px;
  }
  .x1:hover{
     transform:translate(2px);
  }
  .blue{
    color: blue;
  }
  .content {
    display: flex;
    flex-direction: column;
    gap: 10px; /* Reduced gap between rows */
  }
  .label {
    font-weight: bold;
    margin-right: 10px;
  }
  .value {
    flex: 1;
  }
  .h2light {
    font-size: 22px;
    color: darkblue;
    font-weight: bold;
    margin-bottom: auto;
  }
  .h2dark {
    font-size: 22px;
    color: black;
    font-weight: bold;
    margin-bottom: auto;
  }

  h2, p, a {
    font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace;
    font-size: 25px;
    font-style: normal;
    font-variant: normal;
    font-weight: 700;
    line-height: 26.4px;
  }
  </style>
  