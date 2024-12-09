<template>
    <!-- Main Content -->
    <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
            <h1>Document Insights</h1>
        </div>
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="pt-3 pb-2 mb-3">
                    <form action="http://localhost:5000/upload" method = "post" enctype="multipart/form-data" >
                        <input type="file" id="document" name="document" accept=".pdf">
                        <button type="submit">Upload PDF</button>
                    </form>
                </div>
                <div class="chat-section">
                    <div class="chat-message" v-for="(message, index) in chatMessages" :key="index" style="display: flex;">
                        <div v-if="message.type === 'question'" class="question-box">
                            <span class="question-text">{{ message.text }}</span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-emoji-smile-fill" viewBox="0 0 16 16">
                                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16M7 6.5C7 7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5M4.285 9.567a.5.5 0 0 1 .683.183A3.5 3.5 0 0 0 8 11.5a3.5 3.5 0 0 0 3.032-1.75.5.5 0 1 1 .866.5A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1-3.898-2.25.5.5 0 0 1 .183-.683M10 8c-.552 0-1-.672-1-1.5S9.448 5 10 5s1 .672 1 1.5S10.552 8 10 8"/>
                            </svg>
                        </div>
                        <div v-if="message.type === 'answer'" class="answer-box">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">
                                <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                                <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
                            </svg>
                            <span class="answer-text">{{ message.text }}</span>
                        </div>
                    </div>
                    <div style="display: flex;">
                        <input
                        class="question-input"
                        type="text"
                        placeholder="Ask a question related to the document..."
                        v-model="newQuestion"
                        @keyup.enter="submitQuestion"
                        />
                        <button @click="submitQuestion" class="question-ask-send">➤</button>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="pt-3 pb-2 mb-3 document-summary-chat">
                    <div class="document-summary"> 
                        <button v-if = 'summary_flag' @click="summary" class="question-ask-send"> Document Sumamry</button>
                        <span> {{ document_summary }}</span>
                    </div>
        
                    
                </div>
            </div>
        </div>
    </main>
  </template>
  
  
  
  <script>

  export default {
    props: {
      project_id: Number,
    },
    data() {
      return {
        chatMessages: [],
        newQuestion: "",
        summary_flag: true,
        document_summary: "",
        instructor_id: localStorage.getItem('user_id')
      };
    },
    methods: {
        async previousChat(){
            let response = await fetch('http://localhost:5000/chat/' + this.instructor_id + '/' + this.project_id, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('token')
                },
            });
            let result = await response.json();
            if (!response.ok) {
                alert(result.error);
                return;
            }
            this.chatMessages = result.response;
        },
    async llm (question) {
    // Call the llm API
    let response = await fetch('http://localhost:5000/ask/' + this.instructor_id + '/' + this.project_id, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token')
        },
        body: JSON.stringify({
        'question' : question
        }),
    })
    let result = await response.json()
    if (!response.ok) {
        alert(result.error)
        return
    }
       return result.response
    },
    async summary () {
        let response = await fetch('http://localhost:5000/ask/' + this.instructor_id + '/' + this.project_id, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token')
        },
        body: JSON.stringify({
        'question' : 'What is the summary of the document ?'
        }),
    })
    let result = await response.json()
    if (!response.ok) {
        alert(result.error)
        return
    }
        this.document_summary = result.response
        this.summary_flag = false
    },
      async submitQuestion() {
        if (this.newQuestion.trim()) {
          this.chatMessages.push({ type: "question", text: this.newQuestion });
          this.chatMessages.push({ type: "answer", text: await this.llm(this.newQuestion) });
          this.newQuestion = "";
        }
      },
    },
    async created() {
        await this.previousChat();
    }
  };
  </script>

    