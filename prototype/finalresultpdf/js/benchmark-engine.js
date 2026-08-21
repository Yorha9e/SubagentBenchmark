
/**
 * SUBAGENT BENCHMARK ENGINE v2.4
 * Decoupled Data Processing, Auto-Sorting, and Delta Engine
 */
class BenchmarkEngine {
  constructor(models) {
    this.models = models || window.BENCHMARK_MASTER_MODELS || [];
  }

  // Get models sorted by short task score
  getShortTaskLeaderboard() {
    return [...this.models].sort((a, b) => (b.shortScore || 16) - (a.shortScore || 16));
  }

  // Get models sorted by long task milestone completion
  getLongTaskLeaderboard() {
    return [...this.models].sort((a, b) => (b.longMilestones || 8) - (a.longMilestones || 8));
  }

  // Get models sorted by Reviewer Debug latency (ascending)
  getReviewerLeaderboard() {
    return [...this.models].sort((a, b) => (parseFloat(a.revLatency || 999) - parseFloat(b.revLatency || 999)));
  }

  // Get models sorted by Critic Blind Audit total score
  getCriticLeaderboard() {
    return [...this.models].sort((a, b) => (b.criticScore || 0) - (a.criticScore || 0));
  }
}

window.BenchmarkEngine = BenchmarkEngine;
