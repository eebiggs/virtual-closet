<script>
  let isLoggedIn = false;
  let userId = null;
  let currentScreen = "login";

  let username = "";
  let password = "";
  let loginMessage = "";

  let regUsername = "";
  let regPassword = "";
  let registerMessage = "";

  let newItem = { name: "", category: "", color: "", season: "" };
  let items = [];
  let addItemMessage = "";

  let analytics = {};
  let analyticsMessage = "";

  // New state for editing an item
  let editItem = null; // When null, not editing; otherwise holds the item object
  
  async function handleLogin() {
    try {
      const response = await fetch("http://gateway-service:5005/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      userId = data.user_id;
      loginMessage = `Welcome, ${username}!`;
      isLoggedIn = true;
      currentScreen = "home";
    } catch (error) {
      loginMessage = error.message;
    }
  }

  async function handleRegister() {
    try {
      const response = await fetch("http://gateway_service:5005/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: regUsername, password: regPassword }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Registration failed");
      }

      registerMessage = "Registration successful! Please log in.";
      currentScreen = "login";
    } catch (error) {
      registerMessage = error.message;
    }
  }

  async function fetchItems() {
    try {
      const response = await fetch(`http://gateway_service:5005/items?user_id=${userId}`);
      if (!response.ok) throw new Error("Failed to fetch items");
      items = await response.json();
    } catch (error) {
      addItemMessage = error.message;
    }
  }

  function handleLogout() {
    userId = null;
    isLoggedIn = false;
    currentScreen = "login";
  }

  async function addItem() {
    try {
      const response = await fetch("http://gateway_service:5005/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          name: newItem.name,
          category: newItem.category,
          color: newItem.color,
          season: newItem.season,
        }),
      });
      if (!response.ok) throw new Error("Failed to add item");

      addItemMessage = "Item added successfully!";
      newItem = { name: "", category: "", color: "", season: "" };
      await fetchItems();
    } catch (error) {
      addItemMessage = error.message;
    }
  }

  async function deleteItem(itemId) {
    try {
      const response = await fetch(`http://gateway_service:5005/items/${itemId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId }),
      });
      if (!response.ok) throw new Error("Failed to delete item");

      addItemMessage = "Item deleted successfully!";
      await fetchItems();
    } catch (error) {
      addItemMessage = error.message;
    }
  }

  // New function to update an existing item
  async function updateItem() {
    if (!editItem || !editItem.id) return;

    try {
      const response = await fetch(`http://gateway_service:5005/items/${editItem.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          name: editItem.name,
          category: editItem.category,
          color: editItem.color,
          season: editItem.season,
        }),
      });
      if (!response.ok) throw new Error("Failed to update item");

      addItemMessage = "Item updated successfully!";
      editItem = null; // Exit edit mode
      await fetchItems();
    } catch (error) {
      addItemMessage = error.message;
    }
  }

  async function fetchAnalytics() {
    try {
      const response = await fetch(`http://gateway_service:5005/analytics?user_id=${userId}`);
      if (!response.ok) throw new Error("Failed to fetch analytics");
      analytics = await response.json();
    } catch (error) {
      analyticsMessage = error.message;
    }
  }

  function navigateTo(screen) {
    currentScreen = screen;
    if (screen === "closet") fetchItems();
    if (screen === "analytics") fetchAnalytics();
  }
</script>

<main>
  <h1>My Virtual Closet</h1>

  {#if currentScreen === "login"}
    <div>
      <h2>Login</h2>
      <input type="text" placeholder="Username" bind:value={username} />
      <input type="password" placeholder="Password" bind:value={password} />
      <button on:click={handleLogin}>Login</button>
      <button on:click={() => navigateTo("register")}>Register</button>
      {#if loginMessage}
        <p>{loginMessage}</p>
      {/if}
    </div>
  {/if}

  {#if currentScreen === "register"}
    <div>
      <h2>Register</h2>
      <input type="text" placeholder="Username" bind:value={regUsername} />
      <input type="password" placeholder="Password" bind:value={regPassword} />
      <button on:click={handleRegister}>Register</button>
      <button on:click={() => navigateTo("login")}>Back to Login</button>
      {#if registerMessage}
        <p>{registerMessage}</p>
      {/if}
    </div>
  {/if}

  {#if isLoggedIn && currentScreen === "home"}
    <div>
      <h2>Welcome, {username}!</h2>
      <button on:click={() => navigateTo("closet")}>Manage/View Closet</button>
      <button on:click={() => navigateTo("analytics")}>View Analytics</button>
      <button on:click={handleLogout}>Logout</button>
    </div>
  {/if}

  {#if currentScreen === "closet"}
    <div>
      <h2>Your Closet</h2>

      <!-- Add new item form -->
      <div>
        <input type="text" placeholder="Item Name" bind:value={newItem.name} />
        <input type="text" placeholder="Category" bind:value={newItem.category} />
        <input type="text" placeholder="Color" bind:value={newItem.color} />
        <input type="text" placeholder="Season" bind:value={newItem.season} />
        <button on:click={addItem}>Add Item</button>
      </div>

      {#if addItemMessage}
        <p>{addItemMessage}</p>
      {/if}

      <!-- Edit item form, if editing -->
      {#if editItem}
        <div>
          <h3>Editing: {editItem.name}</h3>
          <input type="text" placeholder="Item Name" bind:value={editItem.name} />
          <input type="text" placeholder="Category" bind:value={editItem.category} />
          <input type="text" placeholder="Color" bind:value={editItem.color} />
          <input type="text" placeholder="Season" bind:value={editItem.season} />
          <button on:click={updateItem}>Update Item</button>
          <button on:click={() => editItem = null}>Cancel</button>
        </div>
      {/if}

      <!-- List of Items -->
      <ul>
        {#each items as item (item.id)}
          <li>
            {item.name} ({item.category} - {item.color} - {item.season})
            <div>
              <button on:click={() => {
                editItem = { ...item }; // Copy item data for editing
              }}>Edit</button>
              <button on:click={() => deleteItem(item.id)}>Delete</button>
            </div>
          </li>
        {/each}
      </ul>

      <button on:click={() => navigateTo("home")}>Back to Home</button>
    </div>
  {/if}

  {#if currentScreen === "analytics"}
    <div>
      <h2>Your Analytics</h2>
      <button on:click={fetchAnalytics}>Refresh Analytics</button>
      {#if analyticsMessage}
        <p>{analyticsMessage}</p>
      {:else if analytics.added !== undefined}
        <ul>
          <li>Items Added: {analytics.added}</li>
          <li>Items Removed: {analytics.removed}</li>
          <li>Items Updated: {analytics.updated}</li>
          <li>Last Updated: {analytics.last_updated}</li>
        </ul>
      {:else}
        <p>Loading analytics...</p>
      {/if}
      <button on:click={() => navigateTo("home")}>Back to Home</button>
    </div>
  {/if}
</main>

<style>
  main {
    font-family: Arial, sans-serif;
    margin: 20px;
  }

  h1, h2 {
    color: #333;
  }

  input {
    margin: 5px 0;
    padding: 8px;
    width: 200px;
    display: block;
  }

  button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    margin: 5px;
  }

  button:hover {
    background-color: #45a049;
  }

  p {
    margin: 10px 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    background-color: #f9f9f9;
    padding: 10px;
    margin: 5px 0;
    border: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  li button {
    background-color: #e74c3c;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
  }

  li button:hover {
    background-color: #c0392b;
  }
</style>
