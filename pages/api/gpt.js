export default function handler(req, res) {
  const { ingredients } = req.body;

  res.status(200).json({
    reply: "Recipe with: " + ingredients.join(", ")
  });
}
