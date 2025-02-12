<template>
  <v-dialog v-model="localVisible" max-width="500px" persistent>
    <v-card>
    
      <v-card-title class="headline">
        {{ isEditMode ? "Edit User" : "Create User" }}
      </v-card-title>

   
      <v-card-text>
        <v-form @submit.prevent="save">
         
          <v-text-field
            v-model="formData.username"
            label="Username"
            :rules="[v => !!v || 'Username is required']"
            required
            outlined
            dense
          ></v-text-field>

          <v-text-field
            v-model="formData.password"
            label="Password"
            type="password"
            :rules="[v => !!v || 'Password is required']"
            required
            outlined
            dense
          ></v-text-field>

            <v-checkbox
            v-for="role in roles"
            :key="role.value"
            v-model="formData.roles"
            :label="role.label"
            :value="role.value"
            multiple
            outlined
            dense
          ></v-checkbox>

       
          <v-text-field
            v-model="formData.preferences.timezone"
            label="Timezone"
            :rules="[v => !!v || 'Timezone is required']"
            required
            outlined
            dense
          ></v-text-field>

        
          <v-switch
            v-model="formData.active"
            label="Active"
            color="primary"
          ></v-switch>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red darken-1" text @click="close">Cancel</v-btn>
        <v-btn color="primary" @click="save">{{ isEditMode ? "Update" : "Create" }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => ({}),
    },
    visible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        username: "",
        password: "",
        roles: [],
        preferences: {
          timezone: "", 
        },
        active: true,
      },
      roles: [
        { label: "Admin", value: "admin" },
        { label: "Manager", value: "manager" },
        { label: "Tester", value: "tester" },
      ],
      localVisible: this.visible,
    };
  },
  computed: {
    isEditMode() {
      return this.user && this.user._id;
    },
  },
  watch: {
   
    visible(newVisible) {
      this.localVisible = newVisible;
    },
    user: {
      immediate: true,
      handler(newUser) {
        if (newUser && newUser._id) {
        
          this.formData = { ...newUser };
      
          if (typeof this.formData.preferences !== "object" || this.formData.preferences === null) {
            this.formData.preferences = { timezone: "" };
          }
        } else {
        
          this.formData = {
            username: "",
            password: "",
            roles: [],
            preferences: {
              timezone: "", 
            },
            active: true,
          };
        }
      },
    },
  },
  methods: {
    save() {
      this.$emit("save", this.formData); 
    },
    close() {
      this.localVisible = false; 
      this.$emit("close");
    },
  },
};
</script>

<style scoped>

.v-card-title {
  background-color: #1976d2; 
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}

.v-btn {
  margin-left: 8px;
  font-family: Arial, Helvetica, sans-serif;
}
.v-switch{
    font-family: Arial, Helvetica, sans-serif;
}
.v-checkbox{
    font-family: Arial, Helvetica, sans-serif;
}
.v-text-field{
    font-family: Arial, Helvetica, sans-serif;
}
</style>