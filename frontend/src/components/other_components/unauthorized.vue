<template>
    <div class="error-page">
      <div class="error-container">
        <h1 class="error-heading">401 Error</h1>
        <p class="error-message">You are not authorized to access this page.</p>
        <router-link to="/" class="btn btn-primary">Back to Home</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Unauthorized'
  }
  </script>
  
  <style scoped>
  .error-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-size: cover;
    background-image: url('../../assets/images/lib_login2.jpg');
    background-repeat: no-repeat;
  }
  
  .error-container {
    text-align: center;
  }
  
  .error-heading {
    font-size: 4rem;
    color: #dc3545; /* Red color for error heading */
  }
  
  .error-message {
    font-size: 1.5rem;
    margin-top: 1rem;
  }
  
  .btn {
    display: inline-block;
    margin-top: 1.5rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: bold;
    text-align: center;
    text-decoration: none;
    color: #fff;
    background-color: #007bff; /* Bootstrap primary color */
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #0056b3; /* Darker shade of primary color on hover */
  }
  </style>
  