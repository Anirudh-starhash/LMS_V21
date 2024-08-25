<template>
  <div :class="[isDarkMode?'dark':'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

      <librarian_header :showStats="false"  :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode"/>


      <div class="main-content">
        <div id="display"></div>
        <h2 :class="[isDarkMode?'h2dark':'h2light']">Book's Created ....</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center"  >Action</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in section_info" :key="book.ISBN">
                  <td scope="col" class="x1"><p>{{book.ISBN}}</p></td>
                  <td scope="col" class="x1"><p>{{book.title}}</p></td>
                  <td scope="col" class="x1" colspace=2>
                      <div class="buttons">
                          <a @click="viewBook(book.ISBN)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye x blue" viewBox="0 0 16 16">
                              <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                              <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                            </svg>
                          </a>
                          <a @click="deletebook(book.ISBN)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3 x red" viewBox="0 0 16 16">
                              <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
                            </svg>
                          </a>
                      </div>
                  </td>
              </tr>
          </tbody>
        </table>
        <div class="d-flex me-5">
          <a @click="AddBook(id)" class="me-5">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-plus-circle-dotted h" viewBox="0 0 16 16" >
              <path d="M8 0q-.264 0-.523.017l.064.998a7 7 0 0 1 .918 0l.064-.998A8 8 0 0 0 8 0M6.44.152q-.52.104-1.012.27l.321.948q.43-.147.884-.237L6.44.153zm4.132.271a8 8 0 0 0-1.011-.27l-.194.98q.453.09.884.237zm1.873.925a8 8 0 0 0-.906-.524l-.443.896q.413.205.793.459zM4.46.824q-.471.233-.905.524l.556.83a7 7 0 0 1 .793-.458zM2.725 1.985q-.394.346-.74.74l.752.66q.303-.345.648-.648zm11.29.74a8 8 0 0 0-.74-.74l-.66.752q.346.303.648.648zm1.161 1.735a8 8 0 0 0-.524-.905l-.83.556q.254.38.458.793l.896-.443zM1.348 3.555q-.292.433-.524.906l.896.443q.205-.413.459-.793zM.423 5.428a8 8 0 0 0-.27 1.011l.98.194q.09-.453.237-.884zM15.848 6.44a8 8 0 0 0-.27-1.012l-.948.321q.147.43.237.884zM.017 7.477a8 8 0 0 0 0 1.046l.998-.064a7 7 0 0 1 0-.918zM16 8a8 8 0 0 0-.017-.523l-.998.064a7 7 0 0 1 0 .918l.998.064A8 8 0 0 0 16 8M.152 9.56q.104.52.27 1.012l.948-.321a7 7 0 0 1-.237-.884l-.98.194zm15.425 1.012q.168-.493.27-1.011l-.98-.194q-.09.453-.237.884zM.824 11.54a8 8 0 0 0 .524.905l.83-.556a7 7 0 0 1-.458-.793zm13.828.905q.292-.434.524-.906l-.896-.443q-.205.413-.459.793zm-12.667.83q.346.394.74.74l.66-.752a7 7 0 0 1-.648-.648zm11.29.74q.394-.346.74-.74l-.752-.66q-.302.346-.648.648zm-1.735 1.161q.471-.233.905-.524l-.556-.83a7 7 0 0 1-.793.458zm-7.985-.524q.434.292.906.524l.443-.896a7 7 0 0 1-.793-.459zm1.873.925q.493.168 1.011.27l.194-.98a7 7 0 0 1-.884-.237zm4.132.271a8 8 0 0 0 1.012-.27l-.321-.948a7 7 0 0 1-.884.237l.194.98zm-2.083.135a8 8 0 0 0 1.046 0l-.064-.998a7 7 0 0 1-.918 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>
          </a>
          <p :class="['x2',isDarkMode?'black':'x2','blue','me-5']">Add Book</p>
        
        </div>
      </div>

      <footer_page/>
  </div>

</template>

<script>
import librarian_header from '../library_components/librarian_header.vue';
import footer_page from '../other_components/footer_page.vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
export default {
   name: "view_section",
   data(){
    return{
      isDarkMode:false,
      section_info:[],
      id:localStorage.getItem("section_id")
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
     AddBook(id){
      this.$router.push({ name: 'add_book', params: { id: id } });
     },
     viewBook(ISBN) {
         localStorage.setItem('book_id', ISBN);
         this.$router.push({ name: 'view_book', params: { id: ISBN } });
      },
      deletebook(ISBN){
        localStorage.setItem("book_id",ISBN);
        this.$router.push({name:'delete_book',params:{id:ISBN}});
      }
   },
   async mounted(){
      const access_token=localStorage.getItem("access_token")
      if(!access_token){
        alert('You have to login first')
        this.$router.push("/librarian_page")
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
            
            const response=await axios.get(`http://127.0.0.1:5000/api/getBooks/${this.id}`)
            // i get response.data.sections is a dictionary 
              this.section_info=response.data.sections
          }
          else{
            localStorage.removeItem("access_token")
            localStorage.removeItem("info")
            this.$router.push("/unauthorized")
          }
          

        }
        catch(error){
          console.log(error)
        }
      }
     },
};
</script> `


<style scoped>
 .left,.right {
   float: left;
   width: 20%; /* The width is 20%, by default */
}
.x2{
  font-size: 25px;
}

 .h{
  height: 40px;
 }
 .h:hover{
  transform: translate(2px);
 }
 .x{
  height: 40px;
  width: 100px;
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
  padding: 20px;
}
h2{
  margin-bottom: auto;
  font-size:20px;;
  color:darkblue;
}
.buttons{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 20px;
}
.blue{
color: blue;
height:30px;
}
.red{
color: red;
height:30px;
}
body {
font-family: 'Arial', sans-serif;
background-color: #f0f0f0;
display: flex;
justify-content: center;
align-items: center;
height: 100vh;
margin: 0;
}
table {
width: 60%;
border-collapse: collapse;
background-color: #fff;
box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
th, td {
padding: 12px 15px;
border: 1px solid #ddd;
text-align: left;
}
th {
background-color: #009879;
color: #fff;
text-transform: uppercase;
}
tr:nth-child(even) {
background-color: #f2f2f2;
}
tr:hover {
background-color: #ddd;
}
h2, p,a {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
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
.black{
color: black;
}
</style>