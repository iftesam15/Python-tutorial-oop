// Shared quiz widget for the Python OOP teaching workspace.
// Markup contract, per question:
// <div class="quiz-q" data-correct="b">
//   <p class="quiz-prompt">...</p>
//   <div class="quiz-opts">
//     <button class="quiz-opt" data-key="a">...</button>
//     <button class="quiz-opt" data-key="b">...</button>
//   </div>
//   <p class="quiz-feedback" data-right="..." data-wrong="..."></p>
// </div>
(function () {
  function initQuiz(root) {
    root.querySelectorAll(".quiz-q").forEach(function (q) {
      var correct = q.getAttribute("data-correct");
      var feedback = q.querySelector(".quiz-feedback");
      var opts = q.querySelectorAll(".quiz-opt");
      var answered = false;

      opts.forEach(function (opt) {
        opt.addEventListener("click", function () {
          if (answered) return;
          answered = true;
          var chosen = opt.getAttribute("data-key");
          var isRight = chosen === correct;

          opts.forEach(function (o) {
            o.disabled = true;
            if (o.getAttribute("data-key") === correct) {
              o.classList.add("quiz-correct");
            }
          });
          if (!isRight) opt.classList.add("quiz-incorrect");

          if (feedback) {
            var msg = isRight
              ? feedback.getAttribute("data-right") || "Correct."
              : feedback.getAttribute("data-wrong") || "Not quite — see the highlighted answer.";
            feedback.textContent = msg;
            feedback.classList.add(isRight ? "quiz-msg-right" : "quiz-msg-wrong");
          }
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-quiz]").forEach(initQuiz);
  });
})();
