<template>
  <div :class="[isDarkMode?'dark':'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

       <!-- header-->
        <librarian_header :showRequests="false"  :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" />


      <div class="main-content">
        <div id="display"></div>
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{request_status}}</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >User Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center" >Requested On</th>
              <th scope="col" class="text-bold" style="text-align:center"  >Action</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in requested_books.slice().reverse()" :key="book.ISBN">
                  <td scope="col"><p>{{book.ISBN}}</p></td>
                  <td scope="col"><p>{{book.user_id}}</p></td>
                  <td scope="col"><p>{{book.title}}</p></td>
                  <td scope="col"><p  class="x3">{{book.request_date}}</p></td>
                  <td scope="col" colspace=2>
                      <div class="buttons">
                          <a @click="grant(book,book.ISBN,book.user_id)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-view-stacked x1 blue" viewBox="0 0 16 16">
                              <path d="M3 0h10a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m0 1a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zm0 8h10a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2m0 1a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1z"/>
                            </svg>
                            <p class="x2">Grant</p>
                          </a>
                          <a @click="reject(book,book.ISBN,book.user_id)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-return-left x1 red" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M14.5 1.5a.5.5 0 0 1 .5.5v4.8a2.5 2.5 0 0 1-2.5 2.5H2.707l3.347 3.346a.5.5 0 0 1-.708.708l-4.2-4.2a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 8.3H12.5A1.5 1.5 0 0 0 14 6.8V2a.5.5 0 0 1 .5-.5"/>
                            </svg>
                            <p class="x2">Reject</p>
                          </a>
                      </div>
                  </td>
              </tr>
          </tbody>
        </table>
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{grant_status}}</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >User Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center" >Granted On</th>
              <th scope="col" class="text-bold" style="text-align:center"  >Action</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in granted_books.slice().reverse()" :key="book.ISBN">
                  <td scope="col" ><p>{{book.ISBN}}</p></td>
                  <td scope="col" ><p>{{book.user_id}}</p></td>
                  <td scope="col" ><p>{{book.title}}</p></td>
                  <td scope="col"><p  class="x3">{{book.issue_date}}</p></td>
                  <td scope="col"  colspace=1>
                      <div class="buttons">
                          <a @click="revoke(book.ISBN,book.user_id)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-return-right x1 green" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M1.5 1.5A.5.5 0 0 0 1 2v4.8a2.5 2.5 0 0 0 2.5 2.5h9.793l-3.347 3.346a.5.5 0 0 0 .708.708l4.2-4.2a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 8.3H3.5A1.5 1.5 0 0 1 2 6.8V2a.5.5 0 0 0-.5-.5"/>
                            </svg>
                            <p class="x2">Revoke Book</p>
                          </a>
                      </div>
                  </td>
              </tr>
          </tbody>
        </table>
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{revoked_status}}</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >User Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center" >Revoked On</th>
              <th scope="col" class="text-bold" style="text-align:center" >Status</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in revoked_books.slice().reverse()" :key="book.ISBN">
                  <td scope="col"><p>{{book.ISBN}}</p></td>
                  <td scope="col"><p>{{book.user_id}}</p></td>
                  <td scope="col" ><p>{{book.title}}</p></td>
                  <td scope="col"><p class="x3">{{book.return_date}}</p></td>
                  <td scope="col"><p class="x3">{{book.status}}</p></td>
              </tr>
          </tbody>
        </table>
       
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
   name: "request_page",
   data(){
    return{
      request_status:'Currently No Requests Received',
      grant_status:'Currently No books Granted!',
      revoked_status:'No Books Revoked yet',
      isDarkMode:false,
      requested_books:[],
      granted_books:[],
      revoked_books:[]
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
    async grant(book,book_id,user_id){
      try{
        const r=await axios.post("http://127.0.0.1:5000/api/grantBook",
          JSON.stringify({
            'user_id':user_id,
            'book_id':book_id
          }),
          {
            headers:{
              'Content-Type':'application/json'
            }
          }
        );

        if(r.status===200){
          const bookIndex = this.requested_books.indexOf(book);
          if (bookIndex !== -1) {
            this.requested_books.splice(bookIndex, 1);
          }
          this.granted_books.push(book)
          // document.getElementById("display").innerHTML='<div class="alert alert-success" role="alert">\
          //     <strong>  Grant Successful </strong>\
          //     reload to see that update!</div>'
          // alert('Grant Successful reload to see that update!')
        }
        else{
          alert('Some Error!');
        }
      }
      catch(error){
        console.log(error)
      }
    },
    async reject(book,book_id,user_id){
      try{
        const r=await axios.post("http://127.0.0.1:5000/api/rejectBook",
          JSON.stringify({
            "user_id":user_id,
            "book_id":book_id
          }),
          {
            headers:{
              'Content-Type':'application/json'
            }
          }
        );
        if(r.status===200){
          const bookIndex = this.requested_books.indexOf(book);
          if (bookIndex !== -1) {
            this.requested_books.splice(bookIndex, 1);
          }
          //  document.getElementById("display").innerHTML='<div class="alert alert-danger" role="alert">\
          //    <strong>  Reject Successful </strong>\
          //     reload to see that!</div>'
          // alert('');
        }
        else{
          alert('Some error!');
        }
      }
      catch(error){
        console.log(error)
      }
    },
    async revoke(book_id,user_id){
      localStorage.setItem("book_id",book_id);
      localStorage.setItem("user_id",user_id);
      this.$router.push({name:"revokeBook",params:{id:book_id}});
    }
   },
   async mounted(){
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
          const response=await axios.get(`http://127.0.0.1:5000/api/getAllRequests`);
          if(response.status===200){
            this.granted_books=response.data["issued_books"];
            this.requested_books=response.data["requested_books"];
            this.revoked_books=response.data["returned_books"];
            if(this.requested_books.length>0){
              this.request_status=`Total Number of requests sent are ${this.requested_books.length}`
            }
            if(this.revoked_books.length>0){
              this.revoked_status=`Total Number of books returned are ${this.revoked_books.length}`
            }
            if(this.granted_books.length>0){
              this.grant_status=`Total Number of issued  books  are ${this.granted_books.length}`
            }
          }
        }
        else{
          localStorage.removeItem("access_token");
          localStorage.removeItem("info");
          localStorage.removeItem("section_id");
          localStorage.removeItem("book_id");
          this.$router.push("/unauthorized")
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
table {
  width: 90%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
  }
  th, td {
  padding: 3px 8px;
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
  p {
    color: darkblue;
    font-size: 18px;
  }
  .x3{
    font-size: 14px;
  }
  .buttons{
    display:flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap:20px;
  }

  .x1,.x2{
    color: #fed7aa;
    text-align: center;
    height: 30px;
    width: 100px;
    font-size: 16px;
  }
  .x1:hover{
    transform: translate(10px);
  }
  .x2{
    color:darkblue;
  }
  .blue{
    color:blue;
  }
  .red{
    color:red;
  }
  .green{
    color:green;
  }
</style>