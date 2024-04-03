<template>
        <div class="table-responsive card rounded-3 p-0 me-5" style="display:flex; justify-content: center; margin:0 60px; margin-top: 20px;">
        <!--Booking 1-->
            <table class="rounded-3 overflow-hidden">
                <tr>
                    <th class="p-3 d-flex justify-content-start" style="background-color: #0DB4F3; padding-right: 20px; padding-left: 20px;">
                        <i style="border-radius:100%; border-color: grey; color: white; background-color: grey;" class="fa fa-user fa-2x fa-border"></i>
                            <p class="h5 my-auto ms-3">Passenger 1
                                <section class="h5 fw-normal my-auto ms-2 ">- Adult</section>
                            </p>
                    </th>
                </tr>
                <tbody class="text-start">
                <tr>
                    <td style="padding-top:20px; padding-left:20px">
                        <!-- Add flight duration -->
                        <h5>Personal details</h5>
                        <div class="row">
                            <div class="col-lg-2 col-sm-2">
                                <select class="form-select " aria-label="Default select example" required>
                                    <option disabled selected value="">Title</option>
                                    <option value="1">Mr.</option>
                                    <option value="2">Mrs.</option>
                                    <option value="3">Ms.</option>
                                    <option value="4">Mdm.</option>
                                </select>
                            </div>
                            <div class="col-lg-4 col-md-2 col-sm-5 ms-5">
                                <input class="text p-1 ps-2" name="firstName" size="30" type="text" placeholder="First/Given name (as in passport)" required>
                            </div>
                            <div class="col-md-4 col-sm-3 ms-3">
                                <input class="text p-1 ps-2" name="lastName" size="30" type="text" placeholder="Last/Family name (as in passport)" required>
                            </div>
                        </div>
                        <h5 class="mt-5">Contact details</h5>
                        <div class="col-2 mb-3">
                            <label for="userEmail" class="form-label">Email address</label>
                            <input type="email" class="form-control" id="userEmail1" required>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
    </div>

</template>
