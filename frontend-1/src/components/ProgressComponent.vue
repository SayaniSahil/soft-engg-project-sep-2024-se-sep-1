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
                        <p>{{ milestone.name }}</p>
                    </div>
                    <div v-if="milestone.status === 'pending'">
                        <div
                            class="circle incomplete mx-auto"
                            :class="{ first: index === 0, last: index === milestones.length - 1 }"
                        ></div>
                        <p>{{ milestone.name }}</p>
                    </div>
                </div>
                <div class="line"></div>
            </div>
        </div>
        <h3>Commit History</h3>
        <div v-if="error" class="error-message">
            <p>Error: {{ error }}</p>
        </div>
        <div v-else-if="loading">
            <p>Loading commit history...</p>
        </div>
        <div v-else>
            <div v-for="(commit, index) in commits" :key="index" class="mb-3">
                <div class="d-flex align-items-center">
                    <div class="circle commit-circle"></div>
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
    data() {
        return {
            commits: [],
            milestones: [
                { id: 1, name: "Milestone 1", status: "completed" },
                { id: 2, name: "Milestone 2", status: "completed" },
                { id: 3, name: "Milestone 3", status: "pending" },
                { id: 4, name: "Milestone 4", status: "pending" },
                { id: 5, name: "Milestone 5", status: "pending" },
            ],
            loading: false,
            error: null,
        };
    },
    props: {
        studentId: {
            type: Number,
            required: true,
        },
    },
    methods: {
        async fetchCommitHistory() {
            this.loading = true;
            this.error = null;

            try {
                // Adjusted API call to pass `studentId` dynamically
                const response = await fetch(
                    `http://127.0.0.1:5000/commit_history/7`,
                    {
                        headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": localStorage.getItem("token"),
                        },

                    }
                );

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();

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
    mounted() {
        this.positionLine();
        this.circleColor();
        this.fetchCommitHistory();
        window.addEventListener("resize", this.positionLine);
    },
    beforeUnmount() {
        window.removeEventListener("resize", this.positionLine);
    },
};
</script>

<style scoped>
.error-message {
    color: red;
    font-weight: bold;
}
</style>
