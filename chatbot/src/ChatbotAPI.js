const key = "PMAK-636ea245489f8e06a0241b13-1e4b74fd03d4787b3419e0532f09b9962e";
const API = {
  GetChatbotResponse: async (message) => {
    return new Promise(function (resolve, reject) {
      setTimeout(function () {
        if (message === "hi") resolve("Welcome to chatbot!");
        else resolve("API call : " + message);
      }, 2000);
    });
  }
};

export default API;
