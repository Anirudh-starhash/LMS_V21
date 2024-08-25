<template>
    <div :class="[isDarkMode?'dark':'main-class']">
      <!-- Bootstrap Link  -->
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
       <!-- User Header -->
      <user_header :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" :showBooks="false"/>
       <!-- Body -->
      <div class="main-content">
        <h2 :class="[isDarkMode?'h2dark':'h2light']">{{book_status}}</h2>
        <ul class="list-unstyled">
          <li v-for="book in books" :key="book.ISBN">
            <div class="card mb-5 color" style="max-width: 500px;">
              <div class="row g-0">
                <div class="col-md-12">
                  <img
                    :src="'../../../src/assets/images/'+book.img_url"
                    class="img-fluid rounded-start img-height"
                    alt="Section Image"
                  />
                </div>
                <div class="col-md-12">
                  <div class="card-body text-start">
                    <div class="book-detail">
                      <span class="value1">{{ book.title }}</span>
                    </div>
                    <div class="book-detail">
                      <span class="label">Book Id:</span>
                      <span class="value">{{ book.ISBN }}</span>
                    </div>
                    <div class="book-detail">
                      <span class="label">Section ID:</span>
                      <span class="value">{{ book.id }}</span>
                    </div>
                    <div class="book-detail">
                      <span class="label">Posted On:</span>
                      <span class="value">{{ book.date }}</span>
                    </div>
                    <div class="book-detail">
                      <span class="label">Author Name:</span>
                      <span class="value">{{ book.auth_fname }} {{ book.auth_lname }}</span>
                    </div>
                    <div class="book-detail">
                      <span class="label">Published By:</span>
                      <span class="value">{{ book.publisher }}</span>
                    </div>
                    <div class="book-detail">
                      <span class="label">No of Pages:</span>
                      <span class="value">{{ book.no_of_pages }}</span>
                    </div>
                    <div class="buttons">
                      <a @click="issue(book.ISBN)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-basket2 x1 blue" viewBox="0 0 16 16">
                          <path d="M4 10a1 1 0 0 1 2 0v2a1 1 0 0 1-2 0zm3 0a1 1 0 0 1 2 0v2a1 1 0 0 1-2 0zm3 0a1 1 0 1 1 2 0v2a1 1 0 0 1-2 0z"/>
                          <path d="M5.757 1.071a.5.5 0 0 1 .172.686L3.383 6h9.234L10.07 1.757a.5.5 0 1 1 .858-.514L13.783 6H15.5a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-.623l-1.844 6.456a.75.75 0 0 1-.722.544H3.69a.75.75 0 0 1-.722-.544L1.123 8H.5a.5.5 0 0 1-.5-.5v-1A.5.5 0 0 1 .5 6h1.717L5.07 1.243a.5.5 0 0 1 .686-.172zM2.163 8l1.714 6h8.246l1.714-6z"/>
                        </svg>
                        <p class="x2">Ask for issuing</p>
                      </a>
                      <a @click="readreview(book.ISBN)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-yelp x1 red" viewBox="0 0 16 16">
                          <path d="m4.188 10.095.736-.17.073-.02A.813.813 0 0 0 5.45 8.65a1 1 0 0 0-.3-.258 3 3 0 0 0-.428-.198l-.808-.295a76 76 0 0 0-1.364-.493C2.253 7.3 2 7.208 1.783 7.14c-.041-.013-.087-.025-.124-.038a2.1 2.1 0 0 0-.606-.116.72.72 0 0 0-.572.245 2 2 0 0 0-.105.132 1.6 1.6 0 0 0-.155.309c-.15.443-.225.908-.22 1.376.002.423.013.966.246 1.334a.8.8 0 0 0 .22.24c.166.114.333.129.507.141.26.019.513-.045.764-.103l2.447-.566zm8.219-3.911a4.2 4.2 0 0 0-.8-1.14 1.6 1.6 0 0 0-.275-.21 2 2 0 0 0-.15-.073.72.72 0 0 0-.621.031c-.142.07-.294.182-.496.37-.028.028-.063.06-.094.089-.167.156-.353.35-.574.575q-.51.516-1.01 1.042l-.598.62a3 3 0 0 0-.298.365 1 1 0 0 0-.157.364.8.8 0 0 0 .007.301q0 .007.003.013a.81.81 0 0 0 .945.616l.074-.014 3.185-.736c.251-.058.506-.112.732-.242.151-.088.295-.175.394-.35a.8.8 0 0 0 .093-.313c.05-.434-.178-.927-.36-1.308M6.706 7.523c.23-.29.23-.722.25-1.075.07-1.181.143-2.362.201-3.543.022-.448.07-.89.044-1.34-.022-.372-.025-.799-.26-1.104C6.528-.077 5.644-.033 5.04.05q-.278.038-.553.104a8 8 0 0 0-.543.149c-.58.19-1.393.537-1.53 1.204-.078.377.106.763.249 1.107.173.417.41.792.625 1.185.57 1.036 1.15 2.066 1.728 3.097.172.308.36.697.695.857q.033.015.068.025c.15.057.313.068.469.032l.028-.007a.8.8 0 0 0 .377-.226zm-.276 3.161a.74.74 0 0 0-.923-.234 1 1 0 0 0-.145.09 2 2 0 0 0-.346.354c-.026.033-.05.077-.08.104l-.512.705q-.435.591-.861 1.193c-.185.26-.346.479-.472.673l-.072.11c-.152.235-.238.406-.282.559a.7.7 0 0 0-.03.314c.013.11.05.217.108.312q.046.07.1.138a1.6 1.6 0 0 0 .257.237 4.5 4.5 0 0 0 2.196.76 1.6 1.6 0 0 0 .349-.027 2 2 0 0 0 .163-.048.8.8 0 0 0 .278-.178.7.7 0 0 0 .17-.266c.059-.147.098-.335.123-.613l.012-.13c.02-.231.03-.502.045-.821q.037-.735.06-1.469l.033-.87a2.1 2.1 0 0 0-.055-.623 1 1 0 0 0-.117-.27Zm5.783 1.362a2.2 2.2 0 0 0-.498-.378l-.112-.067c-.199-.12-.438-.246-.719-.398q-.644-.353-1.295-.695l-.767-.407c-.04-.012-.08-.04-.118-.059a2 2 0 0 0-.466-.166 1 1 0 0 0-.17-.018.74.74 0 0 0-.725.616 1 1 0 0 0 .01.293c.038.204.13.406.224.583l.41.768q.341.65.696 1.294c.152.28.28.52.398.719q.036.057.068.112c.145.239.261.39.379.497a.73.73 0 0 0 .596.201 2 2 0 0 0 .168-.029 1.6 1.6 0 0 0 .325-.129 4 4 0 0 0 .855-.64c.306-.3.577-.63.788-1.006q.045-.08.076-.165a2 2 0 0 0 .051-.161q.019-.083.029-.168a.8.8 0 0 0-.038-.327.7.7 0 0 0-.165-.27"/>
                        </svg>
                        <p class="x2">Read reviews</p>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
            
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
      name: "particular_book",
      data(){
        return{
          isDarkMode:false,
          books:[],
          id:""
  
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
        readreview(book_id){
          localStorage.setItem("book_id",book_id);
          this.$router.push({name:"read_reviews",params:{user_id:this.id,id:book_id}});
        },
        async issue(book_id){
          try{
            const r=await axios.post("http://127.0.0.1:5000/api/request_book",
              JSON.stringify({
                "user_id":this.id,
                "book_id":book_id
              }),
              {
                headers:{
                  'Content-Type':'application/json'
                }
              });
  
              if(r.status===200){
                alert('request sent successfully!')
              }
              else if(r.status===202){
                alert('Max requests sent!')
              }
              else{
                alert('Can\'t request a book already requested / issued')
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
            if(r.status===200){
              const response=await axios.get(`http://127.0.0.1:5000/api/getParticularBook/${this.$route.params.book_name}`);
              this.books=response.data.books;
              this.book_status=`Here is The Information of this Book  ( ${this.$route.params.book_name} )`
            
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
      }
    };
  </script> 
  
  
  <style scoped>
    .x{
        color: #fed7aa;
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
    .blue{
      color:blue;
      font-size: 30px;
    }
    .red{
      color:red;
      font-size: 30px;
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
    .buttons{
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      gap:20px;
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
    color: black;
    }
    h5{
      color:darkblue;
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
    h2,p,a,span {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
    .card-body.text-start .book-detail {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-bottom: 20px;
    }
    .card{
      background-color: aliceblue;
      gap:20px;
    }
    .x1:hover{
      transform:translate(2px);
    }
    span{
      font-size: 20px;;
    }
    .label {
      min-width: 130px;
      color:black;
    }
    .value{
      color:darkblue;
    }
    .value1{
      color:red;
    }
    .img-height {
      height: 450px;
      width:400px; /* Adjust the height of the image */
      object-fit: cover;
    }
    .list-unstyled{
      display: grid;
      grid-template-columns: 1fr;
      gap: 30px;
    }
  </style>