from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import select
from app.db import Session
from app.models import Product
from . import bp
from .forms import ProductForm

@bp.route("/")
@login_required
def lista_produtos():
    with Session() as db:
        products = db.execute(select(Product).order_by(Product.id.desc())).scalars().all()
    return render_template("products/lista_produtos.html", products=products)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        with Session() as db:
            product = Product(
                name=form.name.data.strip(),
                description=form.description.data.strip() if form.description.data else None,
                quantity=form.quantity.data,
                price=form.price.data,
            )
            db.add(product); db.commit()
            flash("Produto criado com sucesso!", "success")
            return redirect(url_for("products.lista_produtos"))
    return render_template("products/formulario_produto.html", form=form, title="Adicionar Produto")

@bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id: int):
    with Session() as db:
        product = db.get(Product, product_id)
        if not product:
            flash("Produto não encontrado.", "warning")
            return redirect(url_for("products.lista_produtos"))
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            product.name = form.name.data.strip()
            product.description = form.description.data.strip() if form.description.data else None
            product.quantity = form.quantity.data
            product.price = form.price.data
            db.commit()
            flash("Produto atualizado!", "success")
            return redirect(url_for("products.lista_produtos"))
    return render_template("products/formulario_produto.html", form=form, title="Editar Produto")

@bp.route("/<int:product_id>/delete", methods=["GET", "POST"])
@login_required
def delete_product(product_id: int):
    with Session() as db:
        product = db.get(Product, product_id)
        if not product:
            flash("Produto não encontrado.", "warning")
            return redirect(url_for("products.lista_produtos"))
        if request.method == "POST":
            db.delete(product); db.commit()
            flash("Produto excluído.", "info")
            return redirect(url_for("products.lista_produtos"))
    return render_template("products/confirma_delete.html", product=product)
