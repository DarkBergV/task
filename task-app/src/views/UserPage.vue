<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>User Details</v-card-title>
      <v-card-text v-if="user">
        
        <v-dialog v-model="showModal" max-width="500px">
          <UserForm
            :user="selectedUser"
            :visible="showModal"
            @save="saveUser"
            @close="closeModal"
          />
        </v-dialog>

        <v-list dense>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><strong>Username:</strong> {{ user.username }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><strong>Roles:</strong> {{ user.roles.join(", ") }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><strong>Timezone:</strong> {{ user.preferences.timezone }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><strong>Active:</strong> 
                <v-chip :color="user.active ? 'green' : 'red'">
                  {{ user.active ? "Yes" : "No" }}
                </v-chip>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><strong>Created At:</strong> {{ formatTimestamp(user.created_ts) }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title><strong>Last Updated At:</strong> {{ formatTimestamp(user.last_updated_ts) }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>

     
        <v-row class="mt-4">
          <v-col>
            <v-btn color="primary" @click="openEditModal(user)">Edit</v-btn>
            <v-btn color="error" @click="deleteUser">Delete</v-btn>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-text v-else>
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <span> Loading user details...</span>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "@/api"; 
import UserForm from "@/components/UserForm.vue"; 

export default {
  props: ["id"], 
  components: { UserForm },
  data() {
    return {
      user: null, 
      showModal: false, 
      selectedUser: null, 
    };
  },
  async created() {
    await this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await apiClient.get(`/users/${this.id}`); 
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    },
    formatTimestamp(timestamp) {
      return new Date(timestamp * 1000).toLocaleString(); 
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
        await this.fetchUser(); 
      } catch (error) {
        console.error("Error saving user:", error);
      }
    },
    closeModal() {
      this.showModal = false; 
    },
    async deleteUser() {
      if (confirm("Are you sure you want to delete this user?")) {
        try {
          await apiClient.delete(`/users/${this.id}`); 
          this.$router.push({ path: "/" }); 
        } catch (error) {
          console.error("Error deleting user:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
.v-card {
  max-width: 600px;
  margin: 20px auto;
}

.v-btn {
  margin-right: 10px;
}
</style>
