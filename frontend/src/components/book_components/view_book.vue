<template>
  <div :class="[isDarkMode?'dark':'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

       <!-- header-->
        <librarian_header :showRequests="false"  :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" />


      <div class="main-content">
         <h1 :class="[isDarkMode?'h2dark':'h2light']">{{book_info.title}}</h1>
         <div class="book_details">
          <div class="book_image">
            <img :src="'../../../src/assets/images/'+book_info.img_url" alt="Book Cover" />
          </div>
          <div class="book-info">
            <p :class="[isDarkMode?'pdark':'plight']"> <span>Author:</span> {{ book_info.auth_fname }} {{ book_info.auth_lname }}</p>
            <p :class="[isDarkMode?'pdark':'plight']"><span>Publisher:</span> {{ book_info.publisher }}</p>
            <p :class="[isDarkMode?'pdark':'plight']"><span>Publication Date:</span> {{ book_info.date }}</p>
            <p :class="[isDarkMode?'pdark':'plight']"><span>Number of Pages:</span> {{ book_info.no_of_pages }}</p>
            <button class="btn btn-primary" @click="viewPdf">View PDF</button>
          </div>
         </div>
         <div class="action-buttons">
          <a @click="editBook(book_info.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square x blue" viewBox="0 0 16 16">
              <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
              <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
            </svg>
          </a>
          <a @click="deletebook(book_info.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3 x red" viewBox="0 0 16 16">
              <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
            </svg>
        </a>
        </div> 

         <!-- PDF Viewer -->
         
          
         
     
         
      </div>

      <!-- Footer -->
      <footer_page/>

      
     
  </div>
  

</template>

<script>
import librarian_header from '../library_components/librarian_header.vue';
import footer_page from '../other_components/footer_page.vue'
import axios from 'axios'
import { useRouter } from 'vue-router';


export default {
   name: "view_book",
   data(){
    return{
      request_status:'Currently No Requests Receive',
      stats_status:'Stats Page is up to date',
      monitor_status:'No Users to Monitor Currently',
      isDarkMode:false,
      id:"",
      book_info:{},
      showPdfViewer: false,
      
    }
   },
   components:{
    librarian_header,
    footer_page,
   }, 
   methods: {
     toggleDarkMode(isDark) {
      this.isDarkMode = isDark;
     },

    editBook(bookId) {
      this.$router.push({ name: 'edit_book', params: { id: bookId } });
    },
    viewPdf(){
      window.open(`${this.book_info.pdf_link}`)
    },
    deletebook(ISBN){
        this.$router.push({name:'delete_book',params:{id:ISBN}});
    }
    
  },
  async mounted(){
    const access_token=localStorage.getItem("access_token")
    if(!access_token){
      alert('You have to login first!')
      this.$router.push("/librarian_page");
    }
    else{
      this.id=localStorage.getItem("book_id");
      try{
        const r=await axios.post("http://127.0.0.1:5000/api/lib_check_permission",null,
          {
            headers:{
              Authorization:`Bearer ${access_token}`
            }
          }
        );
        if(r.status==200){
          const response=await axios.get(`http://127.0.0.1:5000/api/getBook/${this.id}`);
          this.book_info=response.data.book_info;
        }
      }
      catch(error){
        console.log(error)
      }
    }
   },
   setup(){
    const router=useRouter();
    return {router}
   },



};
</script> 


<style scoped>

 .left,.right {
   float: left;
   width: 20%; /* The width is 20%, by default */
} 
.x{
  height: 40px;
  width: 100px;
 }
 .blue{
  color: blue;
  height:30px;
 }
 .red{
  color: red;
  height:30px;
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
.book-info{
  box-sizing: border-box;
  box-shadow: 0 0 15px grey;
  height: auto;
  background-color: aliceblue;
  cursor: pointer;
  padding: 50px;
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
  font-size:30px;;
  color:darkblue;
  font-weight: bold;
  margin-bottom: auto;
}
.h2dark{
  font-size:30px;;
  color:black;
  font-weight: bold;
  margin-bottom: auto;
}

h1,p,span,a {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
.book_details {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 40px;
}
span{
  color: red;
  font-size: 20px;
}
.book_image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}


.book_image img {
  width: 100%;
  height: 15em;
  border-radius: 8px;
  object-fit: cover;
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;
}
.plight{
  font-size:20px;
  color:blue;
}
.pdark{
  font-size: 20px;
  color:darkblue;
}
.pdark span{
  color:red;
}
.action-buttons {
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
  background-color: aliceblue;
  padding:20px;
}

.book_image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.book_image img {
  width: 100%;
  height: 20em;
  border-radius: 8px;
  object-fit: cover;
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;
}

.plight {
  font-size: 20px;
  color: blue;
}

.pdark {
  font-size: 20px;
  color: darkblue;
}

.pdark span {
  color: red;
}

.action-buttons {
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
  background-color: aliceblue;
  padding: 20px;
}

.pdf-viewer-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.pdf-viewer-modal-content {
  background-color: #fff;
  padding: 20px;
  max-width: 80%;
  max-height: 80%;
  overflow: auto;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}
</style>