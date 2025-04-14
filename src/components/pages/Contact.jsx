
import React, { useState, useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import emailjs from 'emailjs-com';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  useEffect(() => {
    AOS.init({ duration: 1000 });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    emailjs.send(
      'service_o3ng71b',        // Remplace par ton service ID
      'template_m5o41xh',       // Remplace par ton template ID
      {
        from_name: formData.name,
        reply_to: formData.email,
        message: formData.message,
      },
      'Z93w-mLKMuZiYOJQp'          // Remplace par ta clé publique EmailJS
    )
    .then((result) => {
      console.log(result.text);
      alert('✅ Message envoyé avec succès !');
      setFormData({ name: '', email: '', message: '' }); // Reset
    })
    .catch((error) => {
      console.error(error.text);
      alert("❌ Une erreur s'est produite. Réessayez.");
    });
  };

  return (
    <div className="bg-[#48CAE4] min-h-screen flex flex-col items-center justify-center mx-auto p-14 md:px-20 lg:px-32 w-full overflow-hidden" id="contact">
      <h1
        className="text-3xl sm:text-5xl font-bold text-center text-[#03045E] mb-12"
        data-aos="fade-down"
      >
        Contactez <span className="underline underline-offset-4 decoration-1 font-light text-[#023E8A]">-Nous</span>
      </h1>
      <p
        className="text-center text-[#0077B6] max-w-80 mb-10"
        data-aos="fade-up"
        data-aos-delay="200"
      >
        Vous avez des questions ou des commentaires ? Remplissez le formulaire ci-dessous, et nous vous répondrons dans les plus brefs délais.
      </p>

      <div
        className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg"
        data-aos="zoom-in"
        data-aos-delay="400"
      >
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium text-[#023E8A]">Nom</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="mt-1 w-full p-3 border border-[#023E8A] rounded-md"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-[#023E8A]">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="mt-1 w-full p-3 border border-[#023E8A] rounded-md"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="message" className="block text-sm font-medium text-[#023E8A]">Message</label>
            <textarea
              id="message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              required
              rows="4"
              className="mt-1 w-full p-3 border border-[#023E8A] rounded-md"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-[#03045E] text-white py-3 rounded-lg hover:bg-[#023E8A] transition duration-300 cursor-pointer"
          >
            Envoyer
          </button>
        </form>
      </div>
    </div>
  );
};

export default Contact;

