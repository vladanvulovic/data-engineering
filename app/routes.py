from datetime import datetime

from flask import jsonify, request

from app.game_stats import get_game_stats
from app.user_stats import get_user_stats


def init_routes(app):
    @app.route('/api/user-stats', methods=['GET'])
    def user_stats():
        """
        API Endpoint: Get user-level statistics.
        Args:
            user_id: The user ID to query.
            date: Optional date filter (YYYY-MM-DD).
        Returns:
            JSON response with user statistics.
        """
        user_id = request.args.get('user_id')
        date = request.args.get('date')
        try:
            if date:
                date = datetime.fromisoformat(date).date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 format (e.g., YYYY-MM-DD)."}), 400

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        try:
            user_statistics = get_user_stats(user_id, date)
            if not user_statistics:
                return jsonify({"error": "No data found for user"}), 404
            return jsonify(user_statistics)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/game-stats', methods=['GET'])
    def game_stats():
        """
        API Endpoint: Get game-level statistics.
        Args:
            date: Optional date filter (YYYY-MM-DD).
        Returns:
            JSON response with user statistics.
        """
        date = request.args.get('date')
        try:
            if date:
                date = datetime.fromisoformat(date).date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 format (e.g., YYYY-MM-DD)."}), 400
        try:
            game_statistics = get_game_stats(date)
            return jsonify(game_statistics)
        except Exception as e:
            return jsonify({"error": str(e)}), 500