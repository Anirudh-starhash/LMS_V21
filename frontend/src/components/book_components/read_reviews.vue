<template>
    <div :class="[isDarkMode?'dark':'main-class']">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <user_header :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode"/>

        <div class="main-content">
          <h2 :class="[isDarkMode?'h2dark':'h2light']">{{response_status}}</h2>
          <div id="display"></div>
          <table>
            <thead>
              <tr>
                <th scope="col" class="text-bold" style="text-align:center" >Book Id</th>
                <th scope="col" class="text-bold" style="text-align:center" >Name</th>
                <th scope="col" class="text-bold" style="text-align:center" >Feedback</th>
                <th scope="col" class="text-bold" style="text-align:center"  >Rating</th>
                <th scope="col" class="text-bold" style="text-align:center"  >Action</th>
              </tr>
            </thead>
            <tbody>
                <tr v-for="x in reviews" :key="x.ISBN">
                    <td scope="col"><p>{{x.ISBN}}</p></td>
                    <td  v-if="x.is_him" scope="col"><p>You</p></td>
                    <td v-else scope="col"><p>{{x.name}}</p></td>
                    <td scope="col"><p>{{x.feedback}}</p></td>
                    <td v-if="x.rating" scope="col"><p>{{x.rating}}/5</p></td>
                    <td v-else scope="col"><p>{{x.rating}}</p></td>
                    <td v-if="x.is_him" scope="col" colspace="2" class="buttons">
                        <div v-if="x.rating">
                            <a @click="editreview(x.user_id,x.ISBN)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square x1 blue" viewBox="0 0 16 16">
                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                </svg>
                            </a>
                            <p>Edit Your Review</p>
                        </div>
                        <div v-if="x.rating">
                            <a @click="deletereview(x.user_id,x.ISBN)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3 x1 red" viewBox="0 0 16 16">
                                    <path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
                                </svg>
                            </a>
                            <p>Delete Your Review</p>
                        </div>
                        <div v-else>
                            <a @click="addreview(x.user_id,x.ISBN)">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-plus-circle-dotted x1 blue" viewBox="0 0 16 16" >
                                    <path d="M8 0q-.264 0-.523.017l.064.998a7 7 0 0 1 .918 0l.064-.998A8 8 0 0 0 8 0M6.44.152q-.52.104-1.012.27l.321.948q.43-.147.884-.237L6.44.153zm4.132.271a8 8 0 0 0-1.011-.27l-.194.98q.453.09.884.237zm1.873.925a8 8 0 0 0-.906-.524l-.443.896q.413.205.793.459zM4.46.824q-.471.233-.905.524l.556.83a7 7 0 0 1 .793-.458zM2.725 1.985q-.394.346-.74.74l.752.66q.303-.345.648-.648zm11.29.74a8 8 0 0 0-.74-.74l-.66.752q.346.303.648.648zm1.161 1.735a8 8 0 0 0-.524-.905l-.83.556q.254.38.458.793l.896-.443zM1.348 3.555q-.292.433-.524.906l.896.443q.205-.413.459-.793zM.423 5.428a8 8 0 0 0-.27 1.011l.98.194q.09-.453.237-.884zM15.848 6.44a8 8 0 0 0-.27-1.012l-.948.321q.147.43.237.884zM.017 7.477a8 8 0 0 0 0 1.046l.998-.064a7 7 0 0 1 0-.918zM16 8a8 8 0 0 0-.017-.523l-.998.064a7 7 0 0 1 0 .918l.998.064A8 8 0 0 0 16 8M.152 9.56q.104.52.27 1.012l.948-.321a7 7 0 0 1-.237-.884l-.98.194zm15.425 1.012q.168-.493.27-1.011l-.98-.194q-.09.453-.237.884zM.824 11.54a8 8 0 0 0 .524.905l.83-.556a7 7 0 0 1-.458-.793zm13.828.905q.292-.434.524-.906l-.896-.443q-.205.413-.459.793zm-12.667.83q.346.394.74.74l.66-.752a7 7 0 0 1-.648-.648zm11.29.74q.394-.346.74-.74l-.752-.66q-.302.346-.648.648zm-1.735 1.161q.471-.233.905-.524l-.556-.83a7 7 0 0 1-.793.458zm-7.985-.524q.434.292.906.524l.443-.896a7 7 0 0 1-.793-.459zm1.873.925q.493.168 1.011.27l.194-.98a7 7 0 0 1-.884-.237zm4.132.271a8 8 0 0 0 1.012-.27l-.321-.948a7 7 0 0 1-.884.237l.194.98zm-2.083.135a8 8 0 0 0 1.046 0l-.064-.998a7 7 0 0 1-.918 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
                                </svg>
                            </a>
                            <p>Re-Add Your Review</p>
                        </div>
                       
                       
                    </td>
                    <td v-else scope="col"><p>Disabled</p></td>


                </tr>
            </tbody>
          </table>
          <div class="buttons">
            <a @click="back">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-backspace x1 red" viewBox="0 0 16 16">
                    <path d="M5.83 5.146a.5.5 0 0 0 0 .708L7.975 8l-2.147 2.146a.5.5 0 0 0 .707.708l2.147-2.147 2.146 2.147a.5.5 0 0 0 .707-.708L9.39 8l2.146-2.146a.5.5 0 0 0-.707-.708L8.683 7.293 6.536 5.146a.5.5 0 0 0-.707 0z"/>
                    <path d="M13.683 1a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-7.08a2 2 0 0 1-1.519-.698L.241 8.65a1 1 0 0 1 0-1.302L5.084 1.7A2 2 0 0 1 6.603 1zm-7.08 1a1 1 0 0 0-.76.35L1 8l4.844 5.65a1 1 0 0 0 .759.35h7.08a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z"/>
                </svg>
            </a>
          </div>

          

            
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
        name:'read_reviews',
        data(){
            return {
                reviews:[],
                id:"",
                user_id:"",
                isDarkMode:false,
                response_status:"",
                is_him:""
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
        async mounted(){
            const access_token=localStorage.getItem("access_token");
            if(!access_token){
                alert('You have to login first!')
                this.$router.push("/login_page");
            }
            else{
                this.id=localStorage.getItem("book_id")
                this.user_id=JSON.parse(localStorage.getItem("info")).id
                try{
                    const r=await axios.post("http://127.0.0.1:5000/api/user_check_permission",null,
                        {
                            headers:{
                                Authorization:`Bearer ${access_token}`
                            }
                        }
                    );

                    if(r.status===200){
                        const response=await axios.get(`http://127.0.0.1:5000/api/getAllReviews/${this.user_id}/${this.id}`);
                        if(response.status===201){
                            this.response_status=response.data.msg;
                        }
                        else{
                        this.reviews=response.data.reviews;
                        this.response_status=`Total Number of reviews for this book = ${this.reviews.length}` 
                    }
                    }
                    else{
                        localStorage.removeItem("access_token")
                        localStorage.removeItem("info");
                        localStorage.removeItem("book_id");
                        this.$router.push("/unauthorized");
                    }
                }
                catch(error){
                    console.log(error);
                }
            }
            
        },
        methods: {
           toggleDarkMode(isDark) {
              this.isDarkMode = isDark;
            },
            back(){
                this.$router.go(-1);
            },
            editreview(user_id,book_id){
                this.$router.push({name:'edit_review',params:{user_id:user_id,book_id:book_id}});
            },
            async deletereview(user_id,book_id){
                try{
                    const r=await axios.post(`http://127.0.0.1:5000/api/deleteReview`,
                        JSON.stringify({
                            'user_id':user_id,
                            'book_id':book_id,
                        }),
                        {
                            headers:{
                                'Content-Type':'application/json'
                            }
                        }
                    );

                    if(r.status===200){
                        document.getElementById("display").innerHTML='<div class="alert alert-danger" role="alert">\
                           <strong>  Deleted Review Successfully </strong>\
                          reload to see that update!</div>'

                        
                        
                        
                    }
                    else{
                        localStorage.removeItem("access_token");
                        localStorage.removeItem("info");
                        localStorage.removeItem("book_id");
                        localStorage.removeItem("section_id");
                        this.$router.push("/unauthorized");
                    }
                }
                catch(error){
                    console.log(error)
                }
            },
            async addreview(user_id,book_id){
                try{
                    const r=await axios.post(`http://127.0.0.1:5000/api/submitReview`,
                        JSON.stringify({
                            'user_id':user_id,
                            'book_id':book_id,
                            'review':'Excellent',
                            'ratings':5
                        }),
                        {
                            headers:{
                                'Content-Type':'application/json'
                            }
                        }
                    );

                    if(r.status===200){
                        document.getElementById("display").innerHTML='<div class="alert alert-danger" role="alert">\
                           <strong>Some random Review Added Back Successfully </strong>\
                          reload to see that update and then edit it!!</div>'

                        
                        
                        
                    }
                    else{
                        localStorage.removeItem("access_token");
                        localStorage.removeItem("info");
                        localStorage.removeItem("book_id");
                        localStorage.removeItem("section_id");
                        this.$router.push("/unauthorized");
                    }
                }
                catch(error){
                    console.log(error)
                }
            }
        },
       
    }
</script>

<style scoped>
.x{
    color: #fed7aa;
}
.x1{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
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
color: red;
}
.main-content{
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
text-align: center;
gap:40px;
padding: 80px;
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

}
.h2dark{
font-size:22px;;
color:black;
font-weight: bold;

}
.h1light{
padding:20px;
font-size:32px;;
color:red;
font-weight: bold;
margin-bottom: auto;
}
.h1dark{
padding:20px;
font-size:32px;;
color:darkblue;
font-weight: bold;
margin-bottom: auto;
}
h1,h2,p,a {font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace; font-size: 25px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 26.4px; }
table {
    width: 110%;
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
      font-size: 14px;
    }
    .buttons{
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      gap:30px;
    }
    .red{
        color:red;
    }
    .blue{
        color:blue;
    }
</style>