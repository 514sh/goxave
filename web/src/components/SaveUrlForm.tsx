const SaveUrlForm = () => {
  return (
    <div className="flex flex-items-center justify-center">
      <form className="p-6 rounded-lg shadow-md flex flex-col gap-6 items-center basis-[66dvw]">
        <input
          className="placeholder-muted border border-border rounded-md w-full px-4 py-2"
          placeholder="Paste url here"
        />
        <button className="font-serif text-white border border-border rounded-md hover:bg-orange transition bg-primary px-4 py-2 text-bold active:bg-orange active:text-white focus:bg-orange focus:text-white">
          Save
        </button>
      </form>
    </div>
  );
};

export default SaveUrlForm;
