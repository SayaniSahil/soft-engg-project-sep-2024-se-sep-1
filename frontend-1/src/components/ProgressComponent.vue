<template>
    <div>
        <div>
            <h2>STATISTICS</h2>
            <div class="milestones d-flex justify-content-between mb-4">
                <div
                    v-for="(milestone, index) in milestones"
                    :key="milestone.id"
                    class="text-center"
                >
                    <div v-if="milestone.status === 'completed'">
                        <div
                            class="circle completed mx-auto"
                            :class="{ first: index === 0, last: index === milestones.length - 1 }"
                        ></div>
                        <p>{{ milestone.title }}</p>
                    </div>
                    <div v-if="milestone.status === 'pending'">
                        <div
                            class="circle incomplete mx-auto"
                            :class="{ first: index === 0, last: index === milestones.length - 1 }"
                        ></div>
                        <p>{{ milestone.title }}</p>
                    </div>
                </div>
                <div class="line"></div>
            </div>
        </div>
        <h3>Commit History</h3>
        <div v-if="error" class="error-message">
            <p>Error: {{ error }}</p>
        </div>
        <div v-else-if="require_url">
            <form>
                <label for="url">Enter the URL of the repository:</label>
                <input type="text" id="url" name="url" v-model="url" required>
                <button @click.prevent="uploadURL">Submit</button>
            </form>
        </div>
        <div v-else-if="loading">
            <p>Loading commit history...</p>
        </div>
        <div v-else>
            <div v-for="(commit, index) in commits" :key="index" class="mb-3">
                <div class="d-flex align-items-center">
                    <div :class="['circle', 'commit-circle', index === 0 ? 'commit-circle-0' : '']"></div>
                    <div>
                        <p><strong>Author:</strong> {{ commit.author_name }}</p>
                        <p><strong>Timestamp:</strong> {{ commit.timestamp }}</p>
                        <a :href="commit.commit_url" target="_blank" class="github-link">
                            View Commit
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        student_id: Number,
    },
    data() {
        return {
            commits: [],
            milestones: [],
            loading: false,
            error: null,
            require_url: false,
            url: "",
        };
    },
    watch: {
    // Watch for changes in student_id
    student_id(newStudentId) {
      this.fetchMilestoneStatus(newStudentId);
      this.fetchCommitHistory(newStudentId);
    },
    milestones(newMilestones) {
        if (newMilestones) {
            this.positionLine();
        }
    },
  },
    methods: {
        async fetchMilestoneStatus() {
            this.loading = true;
            this.error = null;
            if (this.student_id === null) {
                this.error = "Student ID not provided.";
                return;
            }
            const response = await fetch('http://localhost:5000/student/milestones/' + this.student_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
            });
            const result = await response.json();
            if (!response.ok) {
                this.error = result.error;
                return;
            }
            this.milestones = result.milestones;
            // Remove milestones with <=0 weightage
            this.milestones = this.milestones.filter((milestone) => milestone.weightage > 0);
        },
        async fetchCommitHistory() {
            this.loading = true;
            this.error = null;

            if (this.student_id === null) {
                this.error = "Student ID not provided.";
                return;
            }

            try {
                // Adjusted API call to pass `studentId` dynamically
                const response = await fetch(
                    `http://127.0.0.1:5000/commit_history/` + this.student_id,
                    {
                        headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": localStorage.getItem("token"),
                        },

                    }
                );
                const data = await response.json();
                //console.log(data);
                if (!response.ok) {
                    if(data.error.includes('URL')){
                        this.require_url = true;
                        //console.log("URL not provided");
                    }
                    //throw new Error(`HTTP error! Status: ${response.status}`);
                    return;
                }

                // Validate the response format
                if (!data.commit_history || !Array.isArray(data.commit_history)) {
                    throw new Error("Invalid response format.");
                }

                this.commits = data.commit_history;
            } catch (error) {
                this.error = error.message || "Failed to fetch commit history.";
            } finally {
                this.loading = false;
            }
        },
        async uploadURL() {
            const response = await fetch('http://localhost:5000/commit_history/' + this.student_id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
                body: JSON.stringify({ url: this.url }),
            });
            const result = await response.json();
            if (!response.ok) {
                this.error = result.error;
                return;
            }
            this.require_url = false;
            await this.fetchCommitHistory();
        },
        positionLine() {
            const firstBox = this.$el.querySelector(".first");
            const lastBox = this.$el.querySelector(".last");
            const line = this.$el.querySelector(".line");

            if (firstBox && lastBox && line) {
                const firstBoxRect = firstBox.getBoundingClientRect();
                const lastBoxRect = lastBox.getBoundingClientRect();
                line.style.top = `${firstBoxRect.top + firstBoxRect.height / 2}px`;
                line.style.left = `${firstBoxRect.left + firstBoxRect.width / 2}px`;
                line.style.width = `${lastBoxRect.left - firstBoxRect.left}px`;
            }
        },
        circleColor() {
            const ele = document.getElementsByClassName("commit-circle");
            if (ele.length) {
                ele[0].style.backgroundColor = "#d88549";
            }
        },
    },
    async created() {
        await this.fetchMilestoneStatus();
        await this.fetchCommitHistory();
        this.positionLine();
    },
};
</script>

<style scoped>
.error-message {
    color: red;
    font-weight: bold;
}
</style>
