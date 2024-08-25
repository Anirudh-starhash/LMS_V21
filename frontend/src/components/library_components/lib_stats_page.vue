<template>
  <div :class="[isDarkMode ? 'dark' : 'main-class']">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    
    <!-- Header -->
    <librarian_header :showSections="false" :showLib="false" :isDarkMode="isDarkMode" @toggleDarkMode="toggleDarkMode" />

    <div class="main-content">
      <h2 :class="[isDarkMode ? 'h2dark' : 'h2light']">{{ stats_status }}</h2>
      
      <!-- Conditionally render PieChart when section_info has data -->
       <div class="com">
        <PieChart v-if="Object.keys(section_info).length" :sectionInfo="section_info" />
        <BarChart v-if="Object.keys(section_info).length" :sectionInfo="section_info" />
      </div>

      <div @click="getreport">
        <button class="btn btn-primary">Get Report</button>
      </div>
     
    </div>

    <!-- Footer -->
    <footer_page/>
  </div>
</template>

<script scoped>
import librarian_header from './librarian_header.vue';
import footer_page from '../other_components/footer_page.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import PieChart from './PieChart.vue';
import BarChart from './BarChart.vue';

export default {
  name: "librarian_dashboard",
  data() {
    return {
      request_status: 'Currently No Requests Receive',
      stats_status: 'Stats Page is up to date',
      monitor_status: 'No Users to Monitor Currently',
      isDarkMode: false,
      section_info: {}, // Initialize as empty
    };
  },
  components: {
    librarian_header,
    footer_page,
    PieChart,
    BarChart
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    toggleDarkMode(isDark) {
      this.isDarkMode = isDark;
    },
    async getreport(){
      try{
        const r=await axios.get("http://127.0.0.1:5000/api/generate_report");
        if(r.status==200){
          result=r.data.result;
          alert(`Report Sent to Mail Check it out ${result}`)
        }
      }
      catch(error){
        console.log(error);
      }
    }
  },
  async mounted() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
      alert('You need to login first to come here!');
      this.$router.push("/librarian_page");
    } else {
      try {
        const r = await axios.post("http://127.0.0.1:5000/api/lib_check_permission", null, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        if (r.status === 200) {
          const response = await axios.get("http://127.0.0.1:5000/api/getDetails");
          this.section_info = response.data.section_info; // Populate section_info with data
        } else {
          localStorage.clear();
          this.$router.push("/unauthorized");
        }
      } catch (error) {
        console.log(error);
      }
    }
  },
};
</script>

<style scoped>
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

.main-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  gap: 40px;
  padding: 60px;
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

.pie-chart,.bar-chart{
  background-color: aliceblue;
  background-size: cover;
  background-position: center;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}

.com{
  display: flex;
  flex-direction: row;
  gap:20px;
}
</style>
