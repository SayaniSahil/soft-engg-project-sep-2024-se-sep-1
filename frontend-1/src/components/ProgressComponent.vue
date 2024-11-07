<template>
    <div>
        <div>
            <h2>STATISTICS</h2>
            <div class="milestones d-flex justify-content-between mb-4">
                <div v-for="(milestone, index) in milestones" :key="milestone.id" class="text-center">
                    <div v-if="milestone.status == 'completed'">
                        <div class="circle completed mx-auto" :class="{ first: index === 0, last: index === milestones.length - 1 }"></div>
                        <p>{{ milestone.name }}</p>
                    </div>
                    <div v-if="milestone.status == 'pending'">
                        <div class="circle incomplete mx-auto" :class="{ first: index === 0, last: index === milestones.length - 1 }"></div>
                        <p>{{ milestone.name }}</p>
                    </div>
                </div>
                <div class="line"></div>
            </div>
        </div>
        <h3>Commit History</h3>
        <div v-for="commit in commits" :key="commit.id" class="mb-3">
            <div class="d-flex align-items-center">
                <div class="circle commit-circle">
                </div>
                <div>
                    <p style="font-weight: bold;">Commit {{ commit.id }}</p>
                    <p style="font-weight: bold;">Time stamp: {{ commit.timestamp }}</p>
                    <a target="_blank" class="github-link">GitHub link</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
        commits: [
            { id: 5, timestamp: '08:36 am 22/08/2024', link: '#' },
            { id: 4, timestamp: '08:36 am 20/08/2024', link: '#' },
            { id: 3, timestamp: '08:36 am 18/08/2024', link: '#' },
            { id: 2, timestamp: '08:36 am 16/08/2024', link: '#' },
            { id: 1, timestamp: '08:36 am 14/08/2024', link: '#' },
        ],
        milestones: [
          { id: 1, name: 'Milestone 1', status: 'completed' },
          { id: 2, name: 'Milestone 2', status: 'completed' },
          { id: 3, name: 'Milestone 3', status: 'pending' },
          { id: 4, name: 'Milestone 4', status: 'pending' },
          { id: 5, name: 'Milestone 5', status: 'pending' },
        ],
        };
    }, methods: {
        positionLine() {
        const firstBox = this.$el.querySelector(".first");
        const lastBox = this.$el.querySelector(".last");
        const line = this.$el.querySelector(".line");

        if (firstBox && lastBox && line) {
            const firstBoxRect = firstBox.getBoundingClientRect();
            const lastBoxRect = lastBox.getBoundingClientRect();
            const containerRect = this.$el.getBoundingClientRect();

            // Position the line from the center of the first box to the center of the last box
            line.style.top = `${firstBoxRect.top + firstBoxRect.height / 2}px`;
            line.style.left = `${firstBoxRect.left + firstBoxRect.width / 2}px`;
            line.style.width = `${lastBoxRect.left - firstBoxRect.left}px`;
        }
    },
        circleColor(){
            let ele = document.getElementsByClassName('commit-circle');
            ele[0].style.backgroundColor = '#d88549';
            console.log(ele);
        }
    },
    mounted() {
    this.positionLine();
    this.circleColor();
       window.addEventListener("resize", this.positionLine);
    },
    beforeUnmount() {
        window.removeEventListener("resize", this.positionLine);
    },
};
</script>

<style>
.circle {
width: 40px;
height: 40px;
border-radius: 50%;
display: inline-block;
margin-right: 10px;
}
.commit-circle {
width: 40px;
height: 40px;
border-radius: 50%;
display: inline-block;
margin-right: 10px;
border: 3px solid #d88549;
}
.commit .commit-circle:nth {
width: 40px;
height: 40px;
border-radius: 50%;
display: inline-block;
margin-right: 10px;
background-color: #d88549;
}
.milestones .circle {
width: 40px;
height: 40px;
border-radius: 50%;
}
.completed{
background-color: #d4ebe8;
border: 3px solid #50a99c; /* Default border to avoid shift */
z-index: 100;
position: relative;
}
.incomplete{
background-color: #eed9da;
border: 3px solid #bf5362; /* Default border to avoid shift */
z-index: 100;
position: relative;
}
.line {
    position: absolute;
  height: 2px;
  background-color: black;
}
.github-link {
  font-size: 0.9rem;
  color: #6a0dad;
  text-decoration: underline;
}
</style>
