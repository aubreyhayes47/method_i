<template>
  <div>
    <label>
      <input type="checkbox" v-model="selectAll" @change="toggleAll" />
      Select All
    </label>
    <ul>
      <li v-for="candidate in candidates" :key="candidate.id">
        <label>
          <input
            type="checkbox"
            :value="candidate.id"
            v-model="selected"
          />
          {{ candidate.name }}
        </label>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "CastingCallList",
  data() {
    return {
      candidates: [],
      selected: [],
      selectAll: false,
    };
  },
  created() {
    this.fetchCandidates();
  },
  methods: {
    async fetchCandidates() {
      try {
        const response = await fetch("/casting-call/candidates");
        const data = await response.json();
        this.candidates = data;
      } catch (error) {
        console.error("Failed to load candidates", error);
      }
    },
    toggleAll() {
      if (this.selectAll) {
        this.selected = this.candidates.map((c) => c.id);
      } else {
        this.selected = [];
      }
    },
  },
  watch: {
    selected(val) {
      this.selectAll = val.length === this.candidates.length;
    },
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0.5rem 0;
}
</style>
