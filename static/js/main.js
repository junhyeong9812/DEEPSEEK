document.addEventListener("DOMContentLoaded", function () {
  // 탭 전환 기능
  const tabs = document.querySelectorAll(".tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      // 탭 활성화
      document
        .querySelectorAll(".tab")
        .forEach((t) => t.classList.remove("active"));
      this.classList.add("active");

      // 콘텐츠 표시
      const tabId = this.getAttribute("data-tab") + "-tab";
      document.querySelectorAll(".tab-content").forEach((content) => {
        content.classList.add("hidden");
      });
      document.getElementById(tabId).classList.remove("hidden");
    });
  });

  // 채팅 기능
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");
  const clearBtn = document.getElementById("clear-btn");
  const chatMessages = document.getElementById("chat-messages");

  if (chatInput && sendBtn && chatMessages) {
    // 메시지 전송 함수
    function sendMessage() {
      const message = chatInput.value.trim();
      if (message === "") return;

      // 사용자 메시지 추가
      addMessage("user", message);
      chatInput.value = "";

      // 로딩 표시
      const loadingId = addMessage("system", "<em>생각 중...</em>");

      // API 요청
      fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: message }),
      })
        .then((response) => response.json())
        .then((data) => {
          // 로딩 메시지 제거
          const loadingMsg = document.getElementById(loadingId);
          if (loadingMsg) loadingMsg.remove();

          // 응답 추가
          if (data.error) {
            addMessage("system", `오류: ${data.error}`);
          } else {
            addMessage("assistant", data.response);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          const loadingMsg = document.getElementById(loadingId);
          if (loadingMsg) loadingMsg.remove();
          addMessage("system", "오류가 발생했습니다. 다시 시도해주세요.");
        });
    }

    // 메시지 추가 함수
    function addMessage(role, content) {
      const messageId = "msg-" + Date.now();
      const messageDiv = document.createElement("div");
      messageDiv.id = messageId;
      messageDiv.className = `message ${role}`;

      // 코드 블록 처리
      let formattedContent = formatMessage(content);

      messageDiv.innerHTML = formattedContent;
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      // 코드 하이라이팅
      if (window.hljs) {
        messageDiv.querySelectorAll("pre code").forEach((block) => {
          hljs.highlightElement(block);
        });
      }

      return messageId;
    }

    // 메시지 포맷팅 (코드 블록)
    function formatMessage(content) {
      // 마크다운 스타일 코드 블록 처리
      const codeBlockRegex = /```(\w+)?\n([\s\S]*?)\n```/g;
      return content.replace(codeBlockRegex, (match, language, code) => {
        language = language || "plaintext";
        return `<pre><code class="language-${language}">${code}</code></pre>`;
      });
    }

    // 이벤트 리스너
    sendBtn.addEventListener("click", sendMessage);

    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // 대화 기록 초기화
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: "clear" }),
        })
          .then((response) => response.json())
          .then((data) => {
            chatMessages.innerHTML = "";
            addMessage(
              "system",
              data.response || "대화 기록이 초기화되었습니다."
            );
          })
          .catch((error) => {
            console.error("Error:", error);
            addMessage("system", "오류가 발생했습니다. 다시 시도해주세요.");
          });
      });
    }
  }

  // 코드 향상 기능
  const enhanceBtn = document.getElementById("enhance-btn");
  const codeInput = document.getElementById("code-input");
  const enhanceTask = document.getElementById("enhance-task");
  const enhanceResult = document.getElementById("enhance-result");

  if (enhanceBtn && codeInput && enhanceTask && enhanceResult) {
    enhanceBtn.addEventListener("click", function () {
      const code = codeInput.value.trim();
      const task = enhanceTask.value;

      if (code === "") {
        enhanceResult.innerHTML = '<p class="error">코드를 입력해주세요.</p>';
        return;
      }

      // 로딩 표시
      enhanceResult.innerHTML =
        '<p class="placeholder"><em>코드 분석 중...</em></p>';

      // API 요청
      fetch("/api/enhance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, task }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            enhanceResult.innerHTML = `<p class="error">오류: ${data.error}</p>`;
          } else {
            // 코드 블록 처리
            let formattedResponse = formatMessage(data.response);
            enhanceResult.innerHTML = formattedResponse;

            // 코드 하이라이팅
            if (window.hljs) {
              enhanceResult.querySelectorAll("pre code").forEach((block) => {
                hljs.highlightElement(block);
              });
            }
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          enhanceResult.innerHTML =
            '<p class="error">오류가 발생했습니다. 다시 시도해주세요.</p>';
        });
    });

    // 메시지 포맷팅 함수는 위와 동일
    function formatMessage(content) {
      const codeBlockRegex = /```(\w+)?\n([\s\S]*?)\n```/g;
      return content.replace(codeBlockRegex, (match, language, code) => {
        language = language || "plaintext";
        return `<pre><code class="language-${language}">${code}</code></pre>`;
      });
    }
  }

  // 음성 입력 버튼
  const voiceInputBtn = document.getElementById("voice-input-btn");
  if (voiceInputBtn && chatInput) {
    voiceInputBtn.addEventListener("click", function () {
      // 여기에 음성 입력 기능 구현 (이후 추가 예정)
      alert("음성 입력 기능은 준비 중입니다.");
    });
  }
});
