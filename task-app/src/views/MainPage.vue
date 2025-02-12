<template>
  <v-container>
    <h1>User Management</h1>
    <v-btn color="primary" @click="openCreateModal">Create User</v-btn>


    <UserForm
      v-if="showModal"
      :user="selectedUser"
      :visible="showModal"
      @save="saveUser"
      @close="closeModal"
    />

 
    <v-table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Roles</th>
          <th>Timezone</th>
          <th>Is Active?</th>
          <th>Last Updated At</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user._id">
          <td>
            <router-link :to="`/user/${user._id}`">{{ user.username }}</router-link>
          </td>
          <td>{{ user.roles.join(", ") }}</td>
          <td>{{ user.preferences.timezone }}</td>
          <td>{{ user.active ? "Yes" : "No" }}</td>
          <td>{{ new Date(user.last_updated_ts * 1000).toLocaleString() }}</td>
          <td>{{ new Date(user.created_ts * 1000).toLocaleString() }}</td>
          <td>
            <v-btn color="primary" @click="openEditModal(user)">Edit</v-btn>
            <v-btn color="error" @click="confirmDelete(user)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import apiClient from "@/api";
import UserForm from "@/components/UserForm.vue"; 

export default {
  components: { UserForm },
  data() {
    return {
      users: [],
      showModal: false,
      selectedUser: null,
    };
  },
  async created() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await apiClient.get("/users"); 
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    openCreateModal() {
      this.selectedUser = null; 
      this.showModal = true;
    },
    openEditModal(user) {
      this.selectedUser = user; 
      this.showModal = true;
    },
    async saveUser(user) {
      try {
        if (user._id) {
          await apiClient.put(`/users/${user._id}`, user);
        } else {
          await apiClient.post("/users", user); 
        }
        this.closeModal();
        await this.fetchUsers(); 
      } catch (error) {
        console.error("Error saving user:", error);
      }
    },
    closeModal() {
      this.showModal = false;
    },
    async confirmDelete(user) {
      if (confirm("Are you sure you want to delete this user?")) {
        try {
          await apiClient.delete(`/users/${user._id}`); 
          await this.fetchUsers();
        } catch (error) {
          console.error("Error deleting user:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}

.v-btn {
  margin-right: 10px;
}
</style>