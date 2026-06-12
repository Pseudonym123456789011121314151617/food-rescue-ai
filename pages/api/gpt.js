const MAX_INGREDIENTS = 20;
const MAX_INGREDIENT_LENGTH = 100;

export default function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { ingredients } = req.body ?? {};

  if (!Array.isArray(ingredients)) {
    return res.status(400).json({ error: "ingredients must be an array" });
  }

  if (ingredients.length === 0 || ingredients.length > MAX_INGREDIENTS) {
    return res
      .status(400)
      .json({ error: `ingredients must contain 1-${MAX_INGREDIENTS} items` });
  }

  for (const item of ingredients) {
    if (typeof item !== "string" || item.length > MAX_INGREDIENT_LENGTH) {
      return res.status(400).json({
        error: `Each ingredient must be a string of at most ${MAX_INGREDIENT_LENGTH} characters`
      });
    }
  }

  const sanitized = ingredients.map((i) => i.trim()).filter(Boolean);

  res.status(200).json({
    reply: "Recipe with: " + sanitized.join(", ")
  });
}
