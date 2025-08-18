const Profile = () => {
  const savedItems = [
    {
      id: 1,
      title:
        "JBL PartyBox 520 Portable battery-powered party speaker with powerful and loud sound",
      currentPrice: "P 20,000",
      details: {},
      imgSrc:
        "https://img.lazcdn.com/g/p/b7e5eafc2115e90139788824936b467a.png_720x720q80.png_.webp",
    },
    {
      id: 2,
      title: "Card Title 2",
      currentPrice: "More descriptive details about another item.",
      details: {},
      imgSrc: "https://via.placeholder.com/100",
    },
    {
      id: 3,
      title: "Card Title 2",
      currentPrice: "More descriptive details about another item.",
      details: {},
      imgSrc: "https://via.placeholder.com/100",
    },
  ];

  return (
    <section className="mx-auto max-w-4xl p-4 sm:p-6">
      <h2 className="mb-6 font-serif text-2xl font-semibold">Saved items</h2>

      <div className="space-y-4">
        {savedItems.map(({ id, imgSrc, title, currentPrice }) => (
          <div
            key={id}
            className="border-border flex flex-col items-center space-y-4 rounded-lg p-4 shadow-sm transition-shadow hover:shadow-md sm:flex-row sm:items-start sm:space-y-0 sm:space-x-4"
          >
            <img
              src={imgSrc}
              alt={title}
              className="h-48 w-full flex-shrink-0 rounded-md object-cover sm:h-24 sm:w-24"
            />

            <div className="text-center sm:text-left">
              <button className="hover:bg-orange active:bg-orange focus:bg-orange w-full rounded px-2 text-left font-serif text-lg font-bold hover:text-white focus:text-white active:text-white">
                {title}
              </button>
              <p className="text-muted mt-1 px-2">
                Current price: {currentPrice}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Profile;
