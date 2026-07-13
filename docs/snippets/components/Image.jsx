export const Image = ({ img, alt, size = "lg" }) => {
  const width = {
    sm: "300px",
    md: "600px",
    lg: "100%",
  }[size] ?? "100%";

  return (
    <Frame>
      <img
        src={img}
        alt={alt}
        style={{ width, maxWidth: "100%", height: "auto", marginInline: "auto" }}
      />
    </Frame>
  );
};
