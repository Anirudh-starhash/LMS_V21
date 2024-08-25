<template>
    <div>
      <h1>Data from Api</h1>
      <div v-if="data"><p>{{data}}</p></div>
      <button @click="axiosDemo">Fetch Data</button>

    </div>
  </template>
  
  <script>
  import axios from 'axios'; // Make sure axios is imported
  
  export default {
    data() {
      return {
        data: null,
      }
    },
    methods: {
      async axiosDemo() {
        try {
          const response = await axios.post("http://127.0.0.1.5000/api/axios",{
          message: "HI"
          })
          if (resp.status == 200){
            console.log(response.status);
            
          }
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      }
    }
  };
  </script>
  