<template>
  <div :class="[isDarkMode?'dark':'main-class']">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
      <user_header :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" :showMyBooks="false"/>
      <div class="main-content">
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{issue_status}}</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center" >Issue Date</th>
              <th scope="col" class="text-bold" style="text-align:center" >Due Date</th>
              <th scope="col" class="text-bold" style="text-align:center"  >Action</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in issued_books.slice().reverse()" :key="book.ISBN">
                  <td scope="col"><p>{{book.ISBN}}</p></td>
                  <td scope="col"><p>{{book.title}}</p></td>
                  <td scope="col"><p>{{book.issue_date}}</p></td>
                  <td scope="col"><p>{{book.due_date}}</p></td>
                  <td scope="col" colspace=2>
                      <div class="buttons">
                          <a @click="viewpdf(book.pdf)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-view-stacked x1 blue" viewBox="0 0 16 16">
                              <path d="M3 0h10a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m0 1a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zm0 8h10a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2m0 1a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1z"/>
                            </svg>
                            <p class="x2">View Pdf</p>
                          </a>
                          <a @click="returnbook(book.ISBN)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-return-left x1 red" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M14.5 1.5a.5.5 0 0 1 .5.5v4.8a2.5 2.5 0 0 1-2.5 2.5H2.707l3.347 3.346a.5.5 0 0 1-.708.708l-4.2-4.2a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 8.3H12.5A1.5 1.5 0 0 0 14 6.8V2a.5.5 0 0 1 .5-.5"/>
                            </svg>
                            <p class="x2">Return Book</p>
                          </a>
                      </div>
                  </td>
              </tr>
          </tbody>
        </table>
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{return_status}}</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center" >Return Date</th>
              <th scope="col" class="text-bold" style="text-align:center"  >Action &nbsp; / &nbsp; Status</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in returned_books.slice().reverse()" :key="book.ISBN">
                  <td scope="col" ><p>{{book.ISBN}}</p></td>
                  <td scope="col" ><p>{{book.title}}</p></td>
                  <td scope="col" ><p>{{book.return_date}}</p></td>
                  <td scope="col"  colspace=1>
                      <div v-if = " book.re_issue" class="buttons">
                          <a  @click="reissue(book,book.ISBN)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-return-right x1 green" viewBox="0 0 16 16">
                              <path fill-rule="evenodd" d="M1.5 1.5A.5.5 0 0 0 1 2v4.8a2.5 2.5 0 0 0 2.5 2.5h9.793l-3.347 3.346a.5.5 0 0 0 .708.708l4.2-4.2a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 8.3H3.5A1.5 1.5 0 0 1 2 6.8V2a.5.5 0 0 0-.5-.5"/>
                            </svg>
                            <p class="x2">Re-issue Book</p>
                          </a>
                          <p>{{book.status}}</p>
                      </div>
                      <div v-else class="buttons">
                        <p>Disabled</p>
                        <p>{{book.status}}</p>
                      </div>
                  </td>
              </tr>
          </tbody>
        </table>
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{request_status}}</h2>
        <table>
          <thead>
            <tr>
              <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
              <th scope="col" class="text-bold" style="text-align:center" >Title</th>
              <th scope="col" class="text-bold" style="text-align:center" >Request Date</th>
              <th scope="col" class="text-bold" style="text-align:center"  >Action</th>
            </tr>
          </thead>
          <tbody>
              <tr v-for="book in requested_books.slice().reverse()" :key="book.ISBN">
                  <td scope="col"><p>{{book.ISBN}}</p></td>
                  <td scope="col" ><p>{{book.title}}</p></td>
                  <td scope="col" ><p>{{book.request_date}}</p></td>
                  <td scope="col"  colspace=1>
                      <div class="buttons">
                          <a @click="withdraw(book,book.ISBN)">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-rocket-takeoff x1 red" viewBox="0 0 16 16">
                              <path d="M9.752 6.193c.599.6 1.73.437 2.528-.362s.96-1.932.362-2.531c-.599-.6-1.73-.438-2.528.361-.798.8-.96 1.933-.362 2.532"/>
                              <path d="M15.811 3.312c-.363 1.534-1.334 3.626-3.64 6.218l-.24 2.408a2.56 2.56 0 0 1-.732 1.526L8.817 15.85a.51.51 0 0 1-.867-.434l.27-1.899c.04-.28-.013-.593-.131-.956a9 9 0 0 0-.249-.657l-.082-.202c-.815-.197-1.578-.662-2.191-1.277-.614-.615-1.079-1.379-1.275-2.195l-.203-.083a10 10 0 0 0-.655-.248c-.363-.119-.675-.172-.955-.132l-1.896.27A.51.51 0 0 1 .15 7.17l2.382-2.386c.41-.41.947-.67 1.524-.734h.006l2.4-.238C9.005 1.55 11.087.582 12.623.208c.89-.217 1.59-.232 2.08-.188.244.023.435.06.57.093q.1.026.16.045c.184.06.279.13.351.295l.029.073a3.5 3.5 0 0 1 .157.721c.055.485.051 1.178-.159 2.065m-4.828 7.475.04-.04-.107 1.081a1.54 1.54 0 0 1-.44.913l-1.298 1.3.054-.38c.072-.506-.034-.993-.172-1.418a9 9 0 0 0-.164-.45c.738-.065 1.462-.38 2.087-1.006M5.205 5c-.625.626-.94 1.351-1.004 2.09a9 9 0 0 0-.45-.164c-.424-.138-.91-.244-1.416-.172l-.38.054 1.3-1.3c.245-.246.566-.401.91-.44l1.08-.107zm9.406-3.961c-.38-.034-.967-.027-1.746.163-1.558.38-3.917 1.496-6.937 4.521-.62.62-.799 1.34-.687 2.051.107.676.483 1.362 1.048 1.928.564.565 1.25.941 1.924 1.049.71.112 1.429-.067 2.048-.688 3.079-3.083 4.192-5.444 4.556-6.987.183-.771.18-1.345.138-1.713a3 3 0 0 0-.045-.283 3 3 0 0 0-.3-.041Z"/>
                              <path d="M7.009 12.139a7.6 7.6 0 0 1-1.804-1.352A7.6 7.6 0 0 1 3.794 8.86c-1.102.992-1.965 5.054-1.839 5.18.125.126 3.936-.896 5.054-1.902Z"/>
                            </svg>
                            <p class="x2">Withdraw Request</p>
                          </a>
                      </div>
                  </td>
              </tr>
          </tbody>
        </table>
        <div id="display"></div>
      </div>
      <footer_page/>
     
  </div>

</template>

<script>
import user_header from '../user_components/user_header.vue' 
import footer_page from '../other_components/footer_page.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
export default {
   name: "user_dashboard",
   data(){
    return{
      request_status:'Currently No Requests Sent',
      stats_status:'Stats Page is up to date',
      issue_status:'No Books Issued Currently',
      return_status:'No Books to return Currently',
      issued_books:[],
      requested_books:[],
      returned_books:[],
      isDarkMode:false,
      id:"",

    }
   },
   setup(){
    const router=useRouter();
    return {router};
   },
   components:{
    user_header,
    footer_page
   },
   methods: {
    toggleDarkMode(isDark) {
     this.isDarkMode = isDark;
    },
    async withdraw(book,book_id){
      try{
        const r=await axios.post("http://127.0.0.1:5000/api/withDrawBook",
          JSON.stringify({
            'user_id':this.id,
            'book_id':book_id
          }),
          {
            headers:{
              'Content-Type':'application/json'
            }
          }
        );

        if(r.status==200){
          const bookIndex = this.requested_books.indexOf(book);
          if (bookIndex !== -1) {
            this.requested_books.splice(bookIndex, 1);
          }
          // document.getElementById("display").innerHTML='<div class="alert alert-danger" role="alert">\
          //    <strong> Withdraw Successful </strong>\
          //     reload to see that update!</div>'
          
          
          this.$router.push({name:'my_books_page', params:{id:this.id}});
        }
      }
      catch(error){
        console.log(error)
      }
    },
    viewpdf(pdf){
      window.open(`${pdf}`)
    },
    returnbook(book_id){
       localStorage.setItem("book_id",book_id);
       this.$router.push(`/returnBook/${book_id}`);
    },
    async reissue(book,book_id){
      try{
        const r=await axios.post("http://127.0.0.1:5000/api/reissue",
          JSON.stringify({
            'user_id':this.id,
            "book_id":book_id
          }),
          {
            headers:{
              'Content-Type':'application/json'
            }
          }
        );

        if(r.status===200){

          const bookIndex = this.returned_books.indexOf(book);
          if (bookIndex !== -1) {
            this.returned_books.splice(bookIndex, 1);
          }

          // Add the book to the requested_book list
          this.requested_books.push(book);

          document.getElementById("display").innerHTML='<div class="alert alert-success" role="alert">\
             <strong>  Re-issued The book Successful </strong>\
              reload to see that update!</div>'
          
          
        }
        else{
          alert('Some Error!')
        }
      }
      catch(error){
        console.log(error)
      }
    }
   },
   async mounted(){
    const access_token=localStorage.getItem("access_token")
    if(!access_token){
      alert('you have to login first!');
      this.$router.push("/login_page");
    }
    else{
        this.id=JSON.parse(localStorage.getItem('info')).id;
        try{
          const r=await axios.post("http://127.0.0.1:5000/api/user_check_permission",null,
            {
              headers:{
                Authorization:`Bearer ${access_token}`
              }
            }
          );
          if(r.status===200){
            const response=await axios.get(`http://127.0.0.1:5000/api/getInfo/${this.id}`);
            if(response.status===200){
              this.issued_books=response.data["issued_books"];
              this.requested_books=response.data["requested_books"];
              this.returned_books=response.data["returned_books"];
              if(this.requested_books.length>0){
                this.request_status=`Total Number of requests sent are ${this.requested_books.length}`
              }
              if(this.returned_books.length>0){
                this.return_status=`Total Number of books returned are ${this.returned_books.length}`
              }
              if(this.issued_books.length>0){
                this.issue_status=`Total Number of issued  books  are ${this.issued_books.length}`
              }
            }
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
   computed:{
    is_reissue(status){
      if(status==1){return true;}
      else{return false;}
    }
   }
};
</script> 


<style scoped>
  .x{
      color: #fed7aa;
  }
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
  .x1:hover{
    transform: translate(10px);
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
h1 {
  color: salmon;
  text-align: center;
  font-family: foglghten;
  font-weight: bold;
  font-size: 40px;
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
.blue{
  color:blue;
}
.red{
  color:red;
}
.green{
  color:green;
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
  .buttons{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap:20px;
  }
</style>