export default function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { ingredients } = req.body || {};

    if (!Array.isArray(ingredients) || ingredients.length === 0) {
      return res
        .status(400)
        .json({ error: "ingredients must be a non-empty array" });
    }

    const invalid = ingredients.find(
      (item) => typeof item !== "string" || item.trim() === ""
    );
    if (invalid !== undefined) {
      return res
        .status(400)
        .json({ error: "Every ingredient must be a non-empty string" });
    }

    res.status(200).json({
      reply: "Recipe with: " + ingredients.join(", "),
    });
  } catch (err) {
    console.error("GPT API error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
}
