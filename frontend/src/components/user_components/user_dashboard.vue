<template>
  <div :class="[isDarkMode ? 'dark' : 'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <user_header :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" />
      
      <h1 :class="[isDarkMode ? 'h1dark' : 'h1light']">Hey {{ name_ }}</h1>
      <div class="container">
          <div class="left-content">
            <form class="d-flex mb-3" @submit.prevent="searchSections">
              <select v-model="selectedSection"  class="custom-select" :disabled="selectDisabled1">
                  <option value="" >Select Section</option>
                  <option v-for="sec in sections" :key="sec.id" :value="sec.name">{{ sec.name }}</option>
              </select>
              <button class="btn btn-success co" type="submit">Search Sections</button>
            </form>
          
            <!-- Second form -->
            <form class="d-flex mb-3" @submit.prevent="searchAuthors">
                <select v-model="selectedAuthor" class="custom-select" :disabled="selectDisabled2">
                    <option value="">Select Author</option>
                    <option v-for="auth in authors" :key="auth.id" :value="auth.name">{{ auth.name }}</option>
                </select>
                <button class="btn btn-success co" type="submit">Search Author Name</button>
            </form>
            
            <!-- Third form -->
            <form class="d-flex mb-3" @submit.prevent="searchBooks">
                <select v-model="selectedBook"   class="custom-select" :disabled="selectDisabled3">
                    <option value="">Select Book</option>
                    <option v-for="book in books" :key="book.id" :value="book.name">{{ book.name }}</option>
                </select>
                <button class="btn btn-success co" type="submit">Search Book Name</button>
            </form>
            <form class="d-flex mb-3" @submit.prevent="setTime" v-if="notSet">
                <select v-model="selectTiming" class="custome-select" :disabled="selectDisabled4">
                    <option value=""></option>
                    <option value="6:00 PM - 6:59 PM">6:00 PM-6:59 PM</option>
                    <option value="7:00 PM - 7:59 PM">7:00 PM-7:59 PM</option>
                    <option value="8:00 PM - 8:59 PM">8:00 PM-8:59 PM</option>
                    <option value="9:00 PM - 9:59 PM">9:00 PM-9:59 PM</option>
                    <option value="10:00 PM - 10:59 PM">10:00 PM-10:59 PM</option>
                    <option value="11:00 PM - 11:59 PM">11:00 PM-11:59 PM</option>
                    <option value="12:00 AM - 00:59 AM">12:00 AM-00:59 AM</option>
                    <option value="1:00 AM - 1:59 AM">1:00 AM-1:59 AM</option>
                    <option value="2:00 AM - 2:59 AM">2:00 AM-2:59 AM</option>
                    <option value="3:00 AM - 3:59 AM">3:00 AM-3:59 AM</option>
                    <option value="4:00 AM - 4:59 AM">4:00 AM-4:59 AM</option>
                    <option value="5:00 AM - 5:59 AM">5:00 AM-5:59 AM</option>
                    <option value="6:00 AM - 6:59 AM">6:00 AM-6:59 AM</option>
                    <option value="7:00 AM - 7:59 AM">7:00 AM-7:59 AM</option>
                    <option value="8:00 AM - 8:59 AM">8:00 AM-8:59 AM</option>
                    <option value="9:00 AM - 9:59 AM">9:00 AM-9:59 AM</option>
                    <option value="10:00 AM - 10:59 AM">10:00 AM-10:59 AM</option>
                    <option value="11:00 AM - 11:59 AM">11:00 AM-11:59 AM</option>
                    <option value="12:00 PM - 12:59 PM">12:00 PM-12:59 PM</option>
                    <option value="1:00 PM - 1:59 PM">1:00 PM-1:59 PM</option>
                    <option value="2:00 PM - 2:59 PM">2:00 PM-2:59 PM</option>
                    <option value="3:00 PM - 3:59 PM">3:00 PM-3:59 PM</option>
                    <option value="4:00 PM - 4:59 PM">4:00 PM-4:59 PM</option>
                    <option value="5:00 PM - 5:59 PM">5:00 PM-5:59 PM</option>
                </select>
                <button class="btn btn-success co" type="submit">Set Timer For Remainder</button>
            </form>
            <div class="d-flex mb-3" v-else>
                <p>Remainder Timing = <br>  <br> <span>{{this.time}}</span><br> <br> <button class="btn btn-primary" @click="editTime">Edit Timings</button></p>
            </div>
          </div>
          <div class="right-content">
              <div class="main-content">
                  <h2 :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ request_status }}</h2>
                  <h2 :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ stats_status }}</h2>
                  <h2 :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ issue_status }}</h2>
                  <h2 :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ return_status }}</h2>
              </div>
          </div>
      </div>
      <footer_page />
  </div>
</template>

<script>
import user_header from '../user_components/user_header.vue' 
import footer_page from '../other_components/footer_page.vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
export default {
   name: "user_dashboard",
   data(){
    return{
      name_: "",
      request_status: 'Check your Requests in my_books Page',
      stats_status: 'Stats Page is up to date',
      issue_status: 'Check Books Issued in my_books page',
      return_status: 'Check Books Returned or to return Currently in my_books',
      isDarkMode: false,
      sections: [],
      books: [],
      authors: [],
      selectedSection: "",
      selectedAuthor: "",
      selectedBook: "",
      selectTiming: "",
      selectDisabled1: false,
      selectDisabled2: false,
      selectDisabled3: false,
      selectDisabled4: false,
      time:""
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
      async searchSections(id) {
         console.log("Searching sections...");
         if(this.selectedSection!=""){
            this.$router.push({name:"particular_sec_books", params:{section_name:this.selectedSection}});
         }
      },
      async searchAuthors() {
         console.log("Searching authors...");
         // Implement your search logic here
         if(this.selectedAuthor!=""){
            const new_name_arr=this.selectedAuthor.split(" ")
            const new_name=new_name_arr[0]+"_"+new_name_arr[1]
            this.$router.push({name:"particular_auth_books", params:{auth_name:new_name}});
         }
      },
      async searchBooks() {
         console.log("Searching books...");
         // Implement your search logic here
         if(this.selectedBook!=""){
            const new_name_arr=this.selectedBook.split(" ")
            const new_name=new_name_arr[0]+"_"+new_name_arr[1]
            this.$router.push({name:"particular_book", params:{book_name:new_name}});
         }
      },
      async setTime() {
         console.log("Setting Time...");
         // Implement your search logic here
         console.log(this.selectTiming)
         if(this.selectTiming!=""){
            const r=await axios.post(`http://127.0.0.1:5000/api/setTiming/${this.$route.params.id}`,
                JSON.stringify({
                    'time':this.selectTiming
                }),
                {
                    headers:{
                        'Content-Type':'application/json'
                    }
                }
            );

            if(r.status==200){
                this.time=r.data.time
                alert('Remainder Updated Check Your mail At that Time')
                if(this.isCurrentTiming(this.time)){
                    const r=await axios.post(`http://127.0.0.1:5000/api/sendEmail/${this.$route.params.id}`)
                    if(r.status===200){
                        alert('You received a email as Current Time is same as Your Remainder Time')
                    }
                }
            }
         }
      },
      editTime(){
        this.time=""
      },
      isCurrentTiming(timeRange){
        const [start, end] = timeRange.split(' - ');
        const [startHour, startMinute, startPeriod] = start.match(/(\d+):(\d+)\s(AM|PM)/).slice(1);
        const [endHour, endMinute, endPeriod] = end.match(/(\d+):(\d+)\s(AM|PM)/).slice(1);

        const currentDate = new Date();
        let currentHour = currentDate.getHours();
        let currentMinute = currentDate.getMinutes();

        // Convert 12-hour format to 24-hour format
        const startHour24 = (startPeriod === 'PM' && startHour !== '12') ? parseInt(startHour) + 12 : (startPeriod === 'AM' && startHour === '12') ? 0 : parseInt(startHour);
        const endHour24 = (endPeriod === 'PM' && endHour !== '12') ? parseInt(endHour) + 12 : (endPeriod === 'AM' && endHour === '12') ? 0 : parseInt(endHour);

        // Create Date objects for start and end times
        const startTime = new Date();
        startTime.setHours(startHour24, startMinute, 0);

        const endTime = new Date();
        endTime.setHours(endHour24, endMinute, 59);

        // Check if current time is between start and end times
        const currentTime = new Date();
        return currentTime >= startTime && currentTime <= endTime;

      }
   },
   watch: {
      selectedSection(value) {
         if (value !== "") {
            this.selectDisabled2 = true;
            this.selectDisabled3 = true;
         } else {
            this.selectDisabled2 = false;
            this.selectDisabled3 = false;
         }
      },
      selectedAuthor(value) {
         if (value !== "") {
            this.selectDisabled1 = true;
            this.selectDisabled3 = true;
         } else {
            this.selectDisabled1 = false;
            this.selectDisabled3 = false;
         }
      },
      selectedBook(value) {
         if (value !== "") {
            this.selectDisabled2 = true;
            this.selectDisabled1 = true;
         } else {
            this.selectDisabled2 = false;
            this.selectDisabled1 = false;
         }
      },
   },
   setup() {
      const router = useRouter();
      return { router };
   },
   async mounted() {
      const access_token = localStorage.getItem("access_token")
      if (!access_token) {
        alert('You have to login first');
        this.$router.push("/login_page");
      } else {
        this.name_ = JSON.parse(localStorage.getItem('info')).name
        try {
          const r = await axios.post("http://127.0.0.1:5000/api/user_check_permission", null, {
            headers: {
              Authorization: `Bearer ${access_token}`
            }
          });
          if (r.status === 200) {
            const response = await axios.get(`http://127.0.0.1:5000/api/getNames`);
            if (response.status === 200) {
              this.sections = response.data.sections
              this.authors = response.data.authors
              this.books = response.data.books
              
            } else {
              alert('Some Error!')
            }
            const res=await axios.get(`http://127.0.0.1:5000/api/getRemainder/${this.$route.params.id}`)
            if(res.status==200){
                this.time=res.data.time;
                if(this.time==""){}
                else{
                   if(this.isCurrentTiming(this.time)){
                    const r=await axios.post(`http://127.0.0.1:5000/api/sendEmail/${this.$route.params.id}`)
                    if(r.status===200){
                        alert('You received a email as Current Time is same as Your Remainder Time')
                    }
                   }
                }
            }
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
    computed:{
        notSet(){
            if(this.time=="") return true;
            else return false;    
        }
    }
};
</script> 

<style scoped>
  .x {
      color: #fed7aa;
  }
  .x1 {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
  span{
    color:black;
  }
  .x:hover {
      background-color: transparent !important;
  }
  .left, .right {
      float: left;
      width: 20%; /* The width is 20%, by default */
  }
  .add {
      margin-top: auto;
  }
  #add { 
      width: 70px; 
      height: 70px; 
      padding: 10px 16px; 
      border-radius: 35px; 
      font-size: 30px; 
      text-align: center; 
  } 
  #add:hover {
      transform: translate(2px);
      background-color: blue;
      color: white;
  }
  .x {
      height: 40px;
      width: 100px;
  }
  .x:hover {
      transform: translate(2px);
      background-color: darkolivegreen;
      color: aliceblue;
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
  .dark {
      display: flex;
      flex-direction: column;
      background-size: cover; 
      background-image: url('../../assets/images/section.jpg');
      background-repeat: no-repeat;
      min-height: 100vh;
  }
  .container {
      display: flex;
  }
  .left-content {
    width: 35%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center; /* Align items vertically centered */
  }
  .right-content {
      width: 70%;
      padding: 20px;
  }
  .main-content {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      gap: 40px;
      padding-bottom: 100px;
      padding-top: 10px;
  }
  .add {
      margin-top: auto;
      width: 200px;
      height: 50px;
  }
  .add:hover {
      transform: translate(2px);
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
  .h1light {
      padding: 20px;
      font-size: 32px;
      color: red;
      font-weight: bold;
      margin-bottom: auto;
  }
  .h1dark {
      padding: 20px;
      font-size: 32px;
      color: darkblue;
      font-weight: bold;
      margin-bottom: auto;
  }
 
  h1, h2, p, a {
      font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; 
      font-size: 25px; 
      font-style: normal; 
      font-variant: normal; 
      font-weight: 700; 
      line-height: 26.4px;
  }
  .custom-select {
      width: 100%;
      max-width: 300px;
  }
  .co{
    width:300px;
  }
</style>
