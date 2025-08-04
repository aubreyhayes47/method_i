<template>
  <div>
    <label>
      <input type="checkbox" v-model="selectAll" @change="toggleAll" />
      Select All
    </label>
    <ul>
      <li
        v-for="(entry, idx) in candidates"
        :key="idx"
        :class="{ warning: entry.candidate.duplicate || entry.candidate.minor_role }"
      >
        <label>
          <input type="checkbox" :value="idx" v-model="selected" />
          {{ entry.candidate.name }}
          <span
            v-if="entry.candidate.duplicate || entry.candidate.minor_role"
            class="warning-icon"
            title="Potential duplicate or minor role"
            >⚠️</span
          >
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
        this.selected = this.candidates.map((_, idx) => idx);
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

.warning-icon {
  color: #e0a800;
  margin-left: 0.25rem;
}

.warning {
  color: #e0a800;
}
</style>
