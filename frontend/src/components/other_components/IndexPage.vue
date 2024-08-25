<template>
  <div class="main-class">
    <!-- Include Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <div class="main_nav container-fluid">
      <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container-fluid">
          <!-- Brand logo or name -->
          <a class="navbar-brand text-dark me-5 co" href="#">Quantum Books</a>

          <!-- Navbar toggle button for mobile -->
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <!-- Links on the left side -->
            <ul class="nvbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item me-3">
                <a class="nav-link active text-dark co" aria-current="page" href="#">Home</a>
              </li>
            </ul>

            <!-- Buttons on the right side -->
            <div class="navig">
              <a href="/librarian_page"><button class="btn btn-primary me-3">Admin</button></a>
              <a href="/login_page"><button class="btn btn-primary">Login</button></a>
            </div>
          </div>
        </div>
      </nav>
    </div>

    <div class="center container">
      <div>
        <h1>LIBRARY MANAGEMENT SYSTEM</h1>
      </div>
      <div class="intro">
        <div class="row1">
          <p><span>&#9733;</span> A multi user library management system</p>
          <p>employing Flask and assisting it with Vue</p>
          <p>along with SQLite for data storage and</p>
          <p>seamless e-book issuance & management</p>
        </div>
        <div class="row1">
          <img src="../../assets/images/lib.jpeg" alt="library_management_system_emblem"
            style="max-width: 100%; height: auto;  border-radius:5%;"
            class="center"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "index_page",
};
</script>

<style scoped>
  .main_nav {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 40px;
    height: 100px;
    background-size: cover;
    background-image: url('../../assets/images/lib_login2.jpg');
    background-repeat: no-repeat;
  }

  .navig {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    gap: 10px;
  }

  h1 {
    color: salmon;
    text-align: center;
    font-family: foglghten;
    font-weight: bold;
    font-size: 40px;
  }

  p, a {
    font-family: "Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace;
    font-size: 24px;
  }

  .co,p{
    color:darkblue;
    font-weight: bold;;
  }

  .center {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 60px;
  }

  .row1 {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .intro {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 60px;
  }

  .main-class {
    display: flex;
    flex-direction: column;
    gap: 60px;
    background-size: cover;
    background-image: url('../../assets/images/lib_login2.png');
    background-repeat: no-repeat;
    min-height: 100vh;
  }

  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  span {
    color: red;
    font-size: 30px;
  }
</style>
